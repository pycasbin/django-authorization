from django.utils.decorators import decorator_from_middleware

from dauthz.middlewares.request_middleware import RequestMiddleware

request_decorator = decorator_from_middleware(RequestMiddleware)
