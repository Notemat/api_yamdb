import os

from django.conf import settings
from reviews.management.commands import data_import
from reviews.models import User


class UserCommand(data_import.Command):
    help = 'Import data from CSV file to Title model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'users.csv')
        )

    def import_data(self, row):
        User.objects.create(
            pk=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio']
        )
