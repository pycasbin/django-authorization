from django.core.management import call_command
from django.test import TestCase

from dauthz.core import enforcer


class TestConfig(TestCase):
    def test_policy_command(self):
        sub = "alice0"
        obj = "book0"
        act = "read"
        assert enforcer.enforce(sub, obj, act) is False
        call_command("policy", "add", sub, obj, act)
        assert enforcer.enforce(sub, obj, act) is True

    def test_role_command(self):
        user = "alice1"
        role = "admin1"

        assert enforcer.has_role_for_user(user, role) is False
        call_command("role", "add", user, role)
        assert enforcer.has_role_for_user(user, role) is True

    def test_group_command(self):
        user = "alice2"
        role = "admin2"
        domain = "group2"
        assert enforcer.has_grouping_policy(user, role) is False
        call_command("group", "add", user, role)
        assert enforcer.has_grouping_policy(user, role) is True

        assert enforcer.has_grouping_policy(user, role, domain) is False
        call_command("group", "add", user, role, domain)
        assert enforcer.has_grouping_policy(user, role, domain) is True
