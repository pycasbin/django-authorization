from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from dauthz.core import enforcer, enforcers

UserModel = get_user_model()


class CasbinBackend(ModelBackend):
    """
    Check permissions with Casbin.
    """

    def __init__(self):
        self.enforcer = enforcer

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)

    def _get_permissions(self, user_obj, obj, from_name):
        """
        Return the direct permissions of `user_obj`
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = f"_{from_name}_perm_cache"
        if not hasattr(user_obj, perm_cache_name):
            policies = self.enforcer.get_implicit_permissions_for_user(user_obj.username)
            perms = tuple(map(tuple, policies))
            setattr(user_obj, perm_cache_name, perms)
        return getattr(user_obj, perm_cache_name)

    def get_user_permissions(self, user_obj, obj=None):
        """
        Return a set of permission the user `user_obj` has from their
        `user_permissions`.
        """
        policies = self.enforcer.get_permissions_for_user(user_obj.username)
        return tuple(map(tuple, policies))

    def get_all_permissions(self, user_obj, obj=None):
        """
        Return a set of permission the user `user_obj` and inherited roles have.
        The result is cached for each user. Refresh By requesting a new instance.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        return self._get_permissions(user_obj, obj, from_name="user")

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_active and super().has_perm(user_obj, perm, obj=obj)

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


def set_enforcer_for_casbin_backend(enforcer_name):
    _enforcer = enforcers[enforcer_name]
    if _enforcer:
        CasbinBackend.enforcer = _enforcer
        CasbinBackend.enforcer.load_policy()
