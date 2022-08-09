from django.utils.decorators import decorator_from_middleware

from dauthz.middlewares.request import RequestMiddleware

request_middleware = decorator_from_middleware(RequestMiddleware)
