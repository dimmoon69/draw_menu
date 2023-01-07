from django.contrib.auth.models import User
from django.core.management import BaseCommand

from _project_.settings import get_secret


class Command(BaseCommand):
    user_data = {
        "username": get_secret('DJANGO_USER_USERNAME'),
        "email": get_secret('DJANGO_USER_EMAIL'),
        "first_name": get_secret('DJANGO_USER_FIRST_NAME'),
        "last_name": get_secret('DJANGO_USER_LAST_NAME'),
    }
    user_password = get_secret('DJANGO_USER_PASSWORD')

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(**self.user_data)
        if created:
            user.is_superuser = True
            user.is_active = True
            user.is_staff = True
            user.set_password(self.user_password)
            user.save()
