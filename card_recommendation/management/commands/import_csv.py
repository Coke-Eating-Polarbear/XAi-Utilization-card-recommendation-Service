# card_recommendation/management/commands/import_csv.py

import csv
from django.core.management.base import BaseCommand
from card_recommendation.models import Card

class Command(BaseCommand):
    help = 'Import CSV data into the Card model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                benefits = eval(row.get('Benefits', '[]'))  # Use eval to parse the list string
                details = eval(row.get('Detail', '[]'))     # Use eval to parse the list string

                Card.objects.create(
                    name=row['Name'],
                    image_url=row.get('Image', ''),
                    link=row.get('Link', ''),
                    benefits=benefits,
                    details=details  # Ensure this matches your model's field name
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
