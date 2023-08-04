import csv

from django.core.management.base import BaseCommand

from foodgram.settings import POS_ONE, POS_ZERO
from recipes.models import Ingredient


class Command(BaseCommand):
    """Load ingredients to the database."""

    help = 'Load ingredients in the database from csv.'

    def handle(self, *args, **options):
        with open('./data/ingredients.csv', 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            ingredients = []
            for row in csv_reader:
                try:
                    create_ingredients = Ingredient(
                        name=row[POS_ZERO],
                        measurement_unit=row[POS_ONE],
                    )
                    ingredients.append(create_ingredients)
                except ValueError:
                    print('Data discrepancy ignored.')
            Ingredient.objects.bulk_create(ingredients)
