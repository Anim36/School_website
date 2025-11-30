from django.core.management.base import BaseCommand
from school.models import Class

class Command(BaseCommand):
    help = 'Create Class 1 to 10'

    def handle(self, *args, **options):
        classes_data = [
            {'name': 'Class 1', 'section': 'A'},
            {'name': 'Class 2', 'section': 'A'},
            {'name': 'Class 3', 'section': 'A'},
            {'name': 'Class 4', 'section': 'A'},
            {'name': 'Class 5', 'section': 'A'},
            {'name': 'Class 6', 'section': 'A'},
            {'name': 'Class 7', 'section': 'A'},
            {'name': 'Class 8', 'section': 'A'},
            {'name': 'Class 9', 'section': 'A'},
            {'name': 'Class 10', 'section': 'A'},
        ]

        created_count = 0
        for class_data in classes_data:
            class_obj, created = Class.objects.get_or_create(
                name=class_data['name'],
                section=class_data['section'],
                defaults=class_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {class_obj}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully created {created_count} classes (Class 1-10)')
        )