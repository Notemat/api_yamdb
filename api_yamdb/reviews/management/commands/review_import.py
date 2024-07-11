import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Review, Title, User


class Command(BaseCommand):
    help = 'Import data from CSV file to Review model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file', type=str,
            default=os.path.join(settings.BASE_DIR,
                                 'static', 'data', 'review.csv')
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            objects = [
                Review(
                    pk=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                for row in reader
            ]

        Review.objects.bulk_create(objects)
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
