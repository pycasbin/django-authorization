from django.http import HttpResponse
from django.test import TestCase

from dauthz.core import enforcer
from dauthz.decorators import enforcer_decorator, request_decorator
from .utils import load_test_policy, make_request


class TestConfig(TestCase):
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
