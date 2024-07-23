import os

from django.conf import settings

from reviews.management.commands import data_import
from reviews.models import Genre, GenreTitle, Title


class GenreTitleCommand(data_import.Command):
    help = 'Import data from CSV file to GenreTitle model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'genre_title.csv')
        )

    def import_data(self, row):
        GenreTitle.objects.create(
            pk=row['id'],
            title=Title.objects.get(pk=row['title_id']),
            genre=Genre.objects.get(pk=row['genre_id'])
        )
