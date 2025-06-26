from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand):
    help = 'Seed the database with courses'

    def handle(self, *args, **kwargs):
        courses = [
            {
                'title': 'File Stream Oriented Programming',
                'description': 'dont you just love fsop',
                'price': 100_000
            },
            {
                'title': 'V8 Engine Exploitation',
                'description': 'get ez bug bounty money',
                'price': 200_000
            },
            {
                'title': 'Rust Programming',
                'description': 'taught by stefanus',
                'price': 150_000
            }
        ]

        Course.objects.all().delete()

        for course in courses:
            Course.objects.update_or_create(
                title=course['title'],
                defaults=course
            )
        
        self.stdout.write('Seeding successful.')