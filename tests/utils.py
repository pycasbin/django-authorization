import os

import mock
from casbin_adapter.models import CasbinRule

import tests.settings as settings
from dauthz.core import enforcer


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
