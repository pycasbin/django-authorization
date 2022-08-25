import mock
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from dauthz.middlewares import EnforcerMiddleware, RequestMiddleware
from .utils import make_request


class TestConfig(TestCase):
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
