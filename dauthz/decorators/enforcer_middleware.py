from django.utils.decorators import decorator_from_middleware

from dauthz.middlewares.enforcer import EnforcerMiddleware

enforcer_middleware = decorator_from_middleware(EnforcerMiddleware)
