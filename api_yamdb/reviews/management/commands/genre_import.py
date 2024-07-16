import os

from django.conf import settings
from reviews.management.commands import data_import
from reviews.models import Genre


class GenreCommand(data_import.Command):
    help = 'Import data from CSV file to Genre model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'genre.csv')
        )

    def import_data(self, row):
        Genre.objects.create(
            pk=row['id'],
            name=row['name'],
            slug=row['slug']
        )
