from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin

from ..core import enforcers, enforcer


class RequestMiddleware(MiddlewareMixin):
    enforcer = None

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self.enforcer = enforcer
        if self.enforcer:
            self.enforcer.load_policy()

    def process_request(self, request):
        if not self.check_permission(request):
            self.require_permission()

    def check_permission(self, request):
        username = request.user.username
        if request.user.is_anonymous:
            username = "anonymous"
        path = request.path
        method = request.method
        return self.enforcer.enforce(username, path, method)

    def require_permission(self):
        raise PermissionDenied


def set_enforcer_for_request_middleware(enforcer_name):
    _enforcer = enforcers[enforcer_name]
    if enforcer:
        RequestMiddleware.enforcer = _enforcer
        RequestMiddleware.enforcer.load_policy()
