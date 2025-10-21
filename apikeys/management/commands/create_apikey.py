from django.core.management.base import BaseCommand
from apikeys.models import APIKey

class Command(BaseCommand):
    help = 'Create a new API key. Usage: python manage.py create_apikey "My key name"'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='?', default='')

    def handle(self, *args, **options):
        name = options['name'] or ''
        key = APIKey.objects.create(name=name)
        self.stdout.write(self.style.SUCCESS('Created API key:'))
        self.stdout.write(key.key)
