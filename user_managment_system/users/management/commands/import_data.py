import json
from django.core.management.base import BaseCommand
from users.models import UsersData

class Command(BaseCommand):
    help = 'Import data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='JSON file to import')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                objs = [
                    UsersData(
                        first_name=e.get('first_name'),
                        last_name=e.get('last_name'),
                        company_name=e.get('company_name'),
                        city=e.get('city'),
                        state=e.get('state'),
                        zip_code=e.get('zip'),
                        email=e.get('email'),
                        web=e.get('web'),
                        user_age=e.get('age'))
                    for e in data
                ]
                UsersData.objects.bulk_create(objs)
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Data import Failed'+str(e)))
