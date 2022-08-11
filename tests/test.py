import os

import casbin
import mock
from casbin_adapter.adapter import Adapter
from casbin_adapter.models import CasbinRule
from django.core.exceptions import PermissionDenied
from django.test import TestCase

import tests.settings as settings
from dauthz.core import enforcers
from dauthz.middlewares.request import RequestMiddleware


def get_fixture(path):
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + path)


def get_enforcer():
    adapter = Adapter()

    CasbinRule.objects.bulk_create(
        [
            CasbinRule(ptype="p", v0="alice", v1="data1", v2="read"),
            CasbinRule(ptype="p", v0="bob", v1="data2", v2="write"),
            CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="read"),
            CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="write"),
            CasbinRule(ptype="g", v0="alice", v1="data2_admin"),
        ]
    )

    return casbin.Enforcer(get_fixture("dauthz-model.conf"), adapter)


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
        request_middleware_enforcer_name = authz_conf["REQUEST_MIDDLEWARE"]["ENFORCER_NAME"]
        request_middleware_enforcer = enforcers.enforcer_list[request_middleware_enforcer_name]
        get_response = mock.MagicMock()
        request_middleware = RequestMiddleware(get_response)
        assert request_middleware.enforcer == request_middleware_enforcer

    def test_request_middleware(self):

        get_response = mock.MagicMock()
        request = make_request(False, "alice0", "/", "GET")
        request_middleware = RequestMiddleware(get_response)

        try:
            request_middleware.process_request(request)
        except PermissionDenied:
            pass
        else:
            self.fail("PermissionDenied not raised")

        request_middleware.enforcer.add_policy("alice0", "/", "GET")
        assert request_middleware.enforcer.enforce("alice0", "/", "GET") is True

        try:
            request_middleware.process_request(request)
        except PermissionDenied:
            self.fail("PermissionDenied shouldn't be raised")
        else:
            pass
