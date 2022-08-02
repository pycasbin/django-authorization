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

import casbin
from casbin_adapter.enforcer import enforcer as proxy_enforcer


class CasbinBackend:
    def __init__(self, use_django_orm_adapter=True, model=None, adapter=None):
        """
        Initialize the enforcer of Casbin backend.
        :param use_django_orm_adapter: whether to use the Django ORM adapter.
        :param model: if not using Django ORM adapter, you should pass the model files as param:model here.
        :param adapter: if not using Django ORM adapter,
                        you should pass the adapter or policy files as param:adapter here.
        """
        self.enforcer = None
        self.use_django_orm_adapter = use_django_orm_adapter
        if use_django_orm_adapter:
            self.enforcer = proxy_enforcer
        else:
            self.enforcer = casbin.Enforcer(model, adapter)

