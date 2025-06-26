from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand):
    help = 'Seed the database with courses'

    def handle(self, *args, **kwargs):
        courses = [
            {
                'title': 'File Stream Oriented Programming',
                'description': 'This module explores what a FILE struct is, how it works, and how this functionality can be exploited to gain read, write, or gain control flow.',
                'price': 100_000,
                'image_path': 'images/courses/gnu.png',
            },
            {
                'title': 'V8 Engine Exploitation',
                'description': 'Chrome V8 exploitation training for beginners',
                'price': 200_000,
                'image_path': 'images/courses/v8.png',
            },
            {
                'title': 'Rust Programming',
                'description': 'Understand ownership, lifetimes, traits, generics, and much more',
                'price': 150_000,
                'image_path': 'images/courses/rust.png',
            }
        ]

        Course.objects.all().delete()

        for course in courses:
            Course.objects.update_or_create(
                title=course['title'],
                defaults=course
            )
        
        self.stdout.write('Seeding successful.')