from django.utils.deprecation import MiddlewareMixin


class RequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
