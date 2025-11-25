import os
import django
import sys

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from accounts.models import User
from school.models import Class, Teacher, Subject


def create_sample_data():
    print("Starting to create sample data...")

    # Create Classes
    classes = []
    for i in range(1, 4):
        class_obj, created = Class.objects.get_or_create(
            name=f"Class {i}",
            section="A"
        )
        classes.append(class_obj)
        if created:
            print(f"✅ Created: {class_obj}")
        else:
            print(f"⚠️ Already exists: {class_obj}")

    # Create Teachers if they don't exist
    teachers_data = [
        {'username': 'math_teacher', 'subject': 'Mathematics', 'first_name': 'John', 'last_name': 'Smith'},
        {'username': 'science_teacher', 'subject': 'Science', 'first_name': 'Sarah', 'last_name': 'Johnson'},
        {'username': 'english_teacher', 'subject': 'English', 'first_name': 'Emily', 'last_name': 'Brown'},
    ]

    teachers = []
    for data in teachers_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': f'{data["username"]}@school.com',
                'user_type': 'teacher',
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✅ Created user: {user.username}")

        teacher, created = Teacher.objects.get_or_create(
            user=user,
            defaults={
                'teacher_id': f'TCH{user.id:04d}',
                'qualification': 'Masters',
                'specialization': data['subject']
            }
        )
        teachers.append(teacher)
        if created:
            print(f"✅ Created teacher: {teacher.user.get_full_name()} - {data['subject']}")
        else:
            print(f"⚠️ Teacher already exists: {teacher.user.get_full_name()}")

    # Create Subjects
    subjects = []
    for class_obj in classes:
        for i, data in enumerate(teachers_data):
            subject_name = f"{data['subject']} - {class_obj.name}"
            subject, created = Subject.objects.get_or_create(
                name=subject_name,
                class_name=class_obj,
                teacher=teachers[i],
            )
            subjects.append(subject)
            if created:
                print(f"✅ Created subject: {subject_name}")
            else:
                print(f"⚠️ Subject already exists: {subject_name}")

    print("\n🎉 Sample data creation completed!")
    print(f"📊 Created: {len(classes)} classes, {len(teachers)} teachers, {len(subjects)} subjects")


if __name__ == '__main__':
    create_sample_data()