from django.core.management import BaseCommand, call_command

from backend.menubar.models import Menu, MenuItem


class Command(BaseCommand):
    help = 'Loads the initial data in to database'

    def handle(self, *args, **options):

        if not Menu.objects.all().exists():
            call_command('loaddata', 'menu', verbosity=0)
            print('Loads the initial data Menu in to database')
        if not MenuItem.objects.all().exists():
            call_command('loaddata', 'menuitem', verbosity=0)
            print('Loads the initial data MenuItem in to database')
