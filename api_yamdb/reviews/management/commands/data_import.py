import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import data from CSV file to model'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.import_data(row)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

    def import_data(self, row):
        pass
