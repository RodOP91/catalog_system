from django.core.management.base import BaseCommand
from catalog_auth.models import *

from django.conf import settings

class Command(BaseCommand):
    help = 'Creando el primer usuario admin'

    def handle(self, *args, **options):
        username = settings.INITIAL_ADMIN_USERNAME
        password = settings.INITIAL_ADMIN_PASSWORD
        email = settings.INITIAL_ADMIN_EMAIL

        admin_user = User.objects.create_user(username=username, password=password)
        admin_user.email=email
        admin_user.is_admin = True
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        token = AuthToken.objects.create(user=admin_user)

        self.stdout.write(self.style.SUCCESS('Usuario admin creado exitosamente.'))
