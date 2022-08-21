import os

import mock
from casbin_adapter.models import CasbinRule
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import TestCase

import tests.settings as settings
from dauthz.core import enforcer
from dauthz.decorators import enforcer_decorator, request_decorator
from dauthz.middlewares import EnforcerMiddleware, RequestMiddleware


def get_fixture(path):
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + path)


def load_test_policy():
    CasbinRule.objects.bulk_create(
        [
            CasbinRule(ptype="p", v0="alice", v1="data1", v2="read"),
            CasbinRule(ptype="p", v0="bob", v1="data2", v2="write"),
            CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="read"),
            CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="write"),
            CasbinRule(ptype="g", v0="alice", v1="data2_admin"),
        ]
    )

    enforcer.load_policy()


authz_conf = getattr(settings, "DAUTHZ")


def make_request(is_anonymous, username, path, method):
    request = mock.Mock()
    request.user = mock.Mock()
    request.user.is_anonymous = is_anonymous
    request.user.username = username
    request.path = path
    request.method = method
    return request


class TestConfig(TestCase):
    def test_default_enforcer(self):
        get_response = mock.MagicMock()

        request_middleware = RequestMiddleware(get_response)
        assert request_middleware.enforcer == enforcer
        enforcer_middleware = EnforcerMiddleware(get_response, "book", "read")
        assert enforcer_middleware.enforcer == enforcer

        assert enforcer.enforce("alice0", "book", "read") is False
        enforcer.add_policy("alice0", "book", "read")
        assert enforcer.enforce("alice0", "book", "read") is True

    def test_request_middleware(self):
        get_response = mock.MagicMock()
        request = make_request(False, "alice1", "/", "GET")
        request_middleware = RequestMiddleware(get_response)

        try:
            request_middleware.process_request(request)
        except PermissionDenied:
            pass
        else:
            self.fail("PermissionDenied not raised")

        request_middleware.enforcer.add_policy("alice1", "/", "GET")
        assert request_middleware.enforcer.enforce("alice1", "/", "GET") is True

        try:
            request_middleware.process_request(request)
        except PermissionDenied:
            self.fail("PermissionDenied shouldn't be raised")
        else:
            pass

    def test_enforcer_middleware(self):
        get_response = mock.MagicMock()
        request = make_request(False, "alice2", "", "")
        enforcer_middleware = EnforcerMiddleware(get_response, "book", "read")

        try:
            enforcer_middleware.process_request(request)
        except PermissionDenied:
            pass
        else:
            self.fail("PermissionDenied not raised")

        enforcer_middleware.enforcer.add_policy("alice2", "book", "read")
        assert enforcer_middleware.enforcer.enforce("alice2", "book", "read") is True

        try:
            enforcer_middleware.process_request(request)
        except PermissionDenied:
            self.fail("PermissionDenied shouldn't be raised")
        else:
            pass

    def test_adapter(self):
        load_test_policy()
        e = enforcer

        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("alice", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "write"))

    def test_request_decorator(self):
        flag = False
        load_test_policy()
        e = enforcer

        @request_decorator
        def func(request):
            nonlocal flag
            flag = True
            return HttpResponse("OK")

        request = make_request(False, "alice3", "/", "GET")
        try:
            response = func(request)
        except:
            pass
        self.assertFalse(flag)
        e.add_policy("alice3", "/", "GET")
        try:
            response = func(request)
        except:
            pass
        self.assertTrue(flag)

    def test_enforcer_decorator(self):
        flag = False
        load_test_policy()
        e = enforcer

        @enforcer_decorator("book", "read")
        def func1(request):
            nonlocal flag
            flag = True
            return HttpResponse("OK")

        @enforcer_decorator("book", "write")
        def func2(request):
            nonlocal flag
            flag = True
            return HttpResponse("OK")

        request = make_request(False, "alice4", "/", "GET")
        try:
            response = func1(request)
        except:
            pass
        self.assertFalse(flag)

        e.add_policy("alice4", "book", "read")
        try:
            response = func1(request)
        except:
            pass
        self.assertTrue(flag)

        flag = False
        request = make_request(False, "alice4", "/", "GET")
        try:
            response = func2(request)
        except:
            pass
        self.assertFalse(flag)

        e.add_policy("alice4", "book", "write")
        try:
            response = func2(request)
        except:
            pass
        self.assertTrue(flag)
