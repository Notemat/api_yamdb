import os

from django.conf import settings

from reviews.management.commands import data_import
from reviews.models import Review, Title, User


class ReviewCommand(data_import.Command):
    help = 'Import data from CSV file to Review model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'review.csv')
        )

    def import_data(self, row):
        Review.objects.create(
            pk=row['id'],
            title=Title.objects.get(pk=row['title_id']),
            text=row['text'],
            author=User.objects.get(pk=row['author']),
            score=row['score'],
            pub_date=row['pub_date']
        )
