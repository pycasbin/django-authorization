from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin

from ..core import enforcers, enforcer


class EnforcerMiddleware(MiddlewareMixin):
    enforcer = None
    obj = None
    act = None

    def __init__(self, get_response, obj=None, act=None):
        super().__init__(get_response)
        self.get_response = get_response
        self.enforcer = enforcer
        if self.enforcer:
            self.enforcer.load_policy()
        self.obj = obj
        self.act = act

    def process_request(self, request):
        if not self.check_permission(request, self.obj, self.act):
            self.require_permission()

    def check_permission(self, request, obj, act):
        username = request.user.username
        if request.user.is_anonymous:
            username = "anonymous"
        return self.enforcer.enforce(username, obj, act)

    def require_permission(self):
        raise PermissionDenied


def set_enforcer_for_enforcer_middleware(enforcer_name):
    _enforcer = enforcers[enforcer_name]
    if _enforcer:
        EnforcerMiddleware.enforcer = _enforcer
        EnforcerMiddleware.enforcer.load_policy()
