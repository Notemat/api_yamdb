import os

from django.conf import settings
from reviews.management.commands import data_import
from reviews.models import Category


class CategoryCommand(data_import.Command):
    help = 'Import data from CSV file to Category model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'category.csv')
        )

    def import_data(self, row):
        Category.objects.create(
            pk=row['id'],
            name=row['name'],
            slug=row['slug']
        )
