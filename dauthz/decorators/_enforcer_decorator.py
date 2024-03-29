from django.utils.decorators import decorator_from_middleware_with_args

from dauthz.middlewares.enforcer_middleware import EnforcerMiddleware

enforcer_decorator = decorator_from_middleware_with_args(EnforcerMiddleware)
