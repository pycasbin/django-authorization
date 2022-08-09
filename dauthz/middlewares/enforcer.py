from django.utils.deprecation import MiddlewareMixin


class EnforcerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
