import os

from django.conf import settings

from reviews.management.commands import data_import
from reviews.models import Comment, Review, User


class CommentsCommand(data_import.Command):
    help = 'Import data from CSV file to Comment model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'comments.csv')
        )

    def import_data(self, row):
        Comment.objects.create(
            pk=row['id'],
            review=Review.objects.get(pk=row['review_id']),
            text=row['text'],
            author=User.objects.get(pk=row['author']),
            pub_date=row['pub_date']
        )
