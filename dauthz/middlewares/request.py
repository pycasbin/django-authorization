from django.utils.deprecation import MiddlewareMixin

class RequestMiddleward(MiddlewareMixin):
    def process_request(self, request):
        pass