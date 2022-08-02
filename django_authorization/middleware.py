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

from django.core.exceptions import PermissionDenied


class AuthorizationMiddleware:
    """
    Authorization Middleware
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # proxy enforcer from casbin_orm_adapter, has been initialized in the adapter
        self.enforcer = None

    def __call__(self, request):
        # Check the permission for each request.
        if not self.check_permission(request):
            # Not authorized, return HTTP 403 error.
            self.require_permission()

        # Permission passed, go to next module.
        response = self.get_response(request)
        return response

    def set_enforcer(self, enforcer):
        self.enforcer = enforcer

    def check_permission(self, request):
        # Customize it based on your authentication method.
        user = request.user.username
        if request.user.is_anonymous:
            user = 'anonymous'
        path = request.path
        method = request.method
        return self.enforcer.enforce(user, path, method)

    def require_permission(self, ):
        raise PermissionDenied
