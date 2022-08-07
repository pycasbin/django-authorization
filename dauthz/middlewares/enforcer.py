from django.utils.deprecation import MiddlewareMixin

class EnforcerMiddleward(MiddlewareMixin):
    def process_request(self, request):
        pass