import mock
from django.test import TestCase

from dauthz.core import enforcer
from dauthz.middlewares import EnforcerMiddleware, RequestMiddleware
from .utils import load_test_policy


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

    def test_adapter(self):
        load_test_policy()
        e = enforcer

        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("alice", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "write"))
