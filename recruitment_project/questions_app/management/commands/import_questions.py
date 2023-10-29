from django.core.management.base import BaseCommand
import csv
from questions_app.models import Question, IQQuestion


class Command(BaseCommand):
    help = 'Import questions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        with open(options['csv_file'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                IQQuestion.objects.create(
                    text=row['Question'],
                    question_type=row['Tag'],
                    option_1=row['Question_choice_1'],
                    option_2=row['Question_choice_2'],
                    option_3=row['Question_choice_3'],
                    option_4=row['Question_choice_4'],
                    correct_answer=row['Correct_answer(s)']
                )
