from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin

from ..core import enforcers, enforcer


class EnforcerMiddleware(MiddlewareMixin):
    enforcer = None

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self.enforcer = enforcer
        if self.enforcer:
            self.enforcer.load_policy()

    def process_request(self, request, obj, act):
        if not self.check_permission(request, obj, act):
            self.require_permission()

    def check_permission(self, request, obj, act):
        username = request.user.username
        if request.user.is_anonymous:
            username = "anonymous"
        return self.enforcer.enforce(username, obj, act)

    def require_permission(self):
        raise PermissionDenied


def set_enforcer_for_enforcer_middleware(enforcer_name):
    enforcer = enforcers[enforcer_name]
    if enforcer:
        EnforcerMiddleware.enforcer = enforcer
        EnforcerMiddleware.enforcer.load_policy()

