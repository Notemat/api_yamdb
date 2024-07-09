import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import User


class Command(BaseCommand):
    help = 'Import data from CSV file to Title model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'users.csv')
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            objects = [
                User(
                    pk=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    about=row['bio']
                )
                for row in reader
            ]

        User.objects.bulk_create(objects)
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
