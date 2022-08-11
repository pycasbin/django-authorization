from django.apps import AppConfig


class DauthzConfig(AppConfig):
    name = 'dauthz'

    def ready(self):
        from .core import init_enforcers

        init_enforcers()
