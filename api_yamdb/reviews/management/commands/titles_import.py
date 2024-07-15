import os

from django.conf import settings
from reviews.management.commands import data_import
from reviews.models import Category, Title


class TitleCommand(data_import.Command):
    help = 'Import data from CSV file to Title model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'titles.csv')
        )

    def import_data(self, row):
        Title.objects.create(
            pk=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(pk=row['category'])
        )
