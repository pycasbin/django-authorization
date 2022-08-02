# Copyright 2022 The Casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import mock
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from django_authorization import AuthorizationMiddleware, CasbinBackend


def get_example(path):
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + path)


class TestConfig(TestCase):
    def test_backend_with_proxy_enforcer(self):
        backend = CasbinBackend(use_django_orm_adapter=True)
        self.assertFalse(backend.enforcer.enforce("alice0", "data1", "read"))
        backend.enforcer.add_policy("alice0", "data1", "read")
        backend.enforcer.save_policy()
        backend.enforcer.load_policy()
        self.assertTrue(backend.enforcer.enforce("alice0", "data1", "read"))
        backend.enforcer.remove_policy("alice0", "data1", "read")
        backend.enforcer.save_policy()

    def test_backend_with_other_enforcer(self):
        backend = CasbinBackend(use_django_orm_adapter=False, model=get_example('rbac_model.conf'),
                                adapter=get_example("rbac_policy.csv"))
        self.assertFalse(backend.enforcer.enforce("alice0", "data1", "read"))
        backend.enforcer.add_policy("alice0", "data1", "read")
        backend.enforcer.save_policy()
        self.assertTrue(backend.enforcer.enforce("alice0", "data1", "read"))
        backend.enforcer.remove_policy("alice0", "data1", "read")
        backend.enforcer.save_policy()

    def test_middleware(self):

        get_response = mock.MagicMock()

        request = mock.Mock()
        request.user = mock.Mock()
        request.user.is_anonymous = False
        request.user.username = "alice0"
        request.path = "/"
        request.method = "GET"

        backend = CasbinBackend(use_django_orm_adapter=True)
        middleware = AuthorizationMiddleware(get_response)
        middleware.set_enforcer(backend.enforcer)

        response = None

        try:
            response = middleware(request)
        except PermissionDenied:
            print(response)
            pass
        else:
            self.fail("PermissionDenied not raised")

        middleware.enforcer.add_policy("alice0", "/", "GET")

        try:
            response = middleware(request)
        except PermissionDenied:
            print(response)
            self.fail("PermissionDenied shouldn't be raised")
        else:
            pass

