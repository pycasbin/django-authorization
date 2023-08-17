from django.contrib.auth.models import User
from django.test import TestCase

from dauthz.core import enforcer


class TestConfig(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.UserModel = User

    def create_users(self):
        self.user = User.objects.create_user(
            username="alice",
            email="test@example.com",
            password="test",
        )

    def setUp(self):
        self.create_users()
        self.e = enforcer

    def test_get_user_permissions(self):
        self.e.clear_policy()
        user = self.UserModel._default_manager.get(pk=self.user.pk)
        self.assertEqual(user.get_user_permissions(), set())
        self.e.add_policy("alice", "data1", "read")
        self.e.add_policy("alice", "data1", "write")
        self.assertEqual(user.get_user_permissions(), {("alice", "data1", "read"), ("alice", "data1", "write")})

    def test_get_all_permissions(self):
        self.e.clear_policy()
        user = self.UserModel._default_manager.get(pk=self.user.pk)
        self.assertEqual(user.get_all_permissions(), set())

        user = self.UserModel._default_manager.get(pk=self.user.pk)
        self.e.add_policy("alice", "data1", "read")
        self.e.add_policy("alice", "data1", "write")
        self.assertEqual(user.get_all_permissions(), {("alice", "data1", "read"), ("alice", "data1", "write")})

        user = self.UserModel._default_manager.get(pk=self.user.pk)  # to reset cache
        self.e.add_policy("data2_admin", "data2", "read")
        self.e.add_policy("data2_admin", "data2", "write")
        self.e.add_role_for_user("alice", "data2_admin")
        self.assertEqual(
            user.get_all_permissions(),
            {
                ("alice", "data1", "read"),
                ("alice", "data1", "write"),
                ("data2_admin", "data2", "write"),
                ("data2_admin", "data2", "read"),
            },
        )

    def test_has_perm(self):
        self.e.clear_policy()
        user = self.UserModel._default_manager.get(pk=self.user.pk)  # to reset cache
        self.assertFalse(user.has_perm(("alice", "data1", "read")))

        user = self.UserModel._default_manager.get(pk=self.user.pk)
        self.e.add_policy("alice", "data1", "read")
        self.assertTrue(user.has_perm(("alice", "data1", "read")))
