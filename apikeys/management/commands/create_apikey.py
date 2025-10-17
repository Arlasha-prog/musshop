import secrets, hashlib
from django.core.management.base import BaseCommand
from apikeys.models import ApiKey

def hash_key(full_key: str):
    return hashlib.sha256(full_key.encode("utf-8")).hexdigest()

class Command(BaseCommand):
    help = "Создать новый API ключ"

    def add_arguments(self, parser):
        parser.add_argument("--name", required=True)
        parser.add_argument("--rate", default="")

    def handle(self, *args, **opts):
        name = opts["name"]
        rate = opts["rate"]
        prefix = secrets.token_urlsafe(6)[:12]
        secret = secrets.token_urlsafe(32)
        full_key = f"{prefix}.{secret}"
        ak = ApiKey.objects.create(name=name, prefix=prefix, hashed_key=hash_key(full_key), rate_limit=rate)
        self.stdout.write(self.style.SUCCESS("API ключ создан!"))
        self.stdout.write(f"NAME: {name}\nPREFIX: {prefix}\nKEY: {full_key}\n")
