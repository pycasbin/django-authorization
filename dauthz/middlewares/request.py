from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin

from ..core import enforcers


class RequestMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

        enforcer_name = getattr(settings, "DAUTHZ")["REQUEST_MIDDLEWARE"]["ENFORCER_NAME"]
        self.enforcer = enforcers.enforcer_list[enforcer_name]

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
