from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Add/Get group policy'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
