import os
import django
import sys

# Add the project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from accounts.models import User
from school.models import SchoolInfo, Class, Teacher, Student, Subject, Notice


def create_sample_data():
    print("Starting to create sample data...")

    # Create School Info
    school, created = SchoolInfo.objects.get_or_create(
        name="Greenwood High School",
        defaults={
            'address': "123 Education Road, Academic City",
            'phone': "+880 1234-567890",
            'email': "info@greenwood.edu"
        }
    )
    if created:
        print(f"✅ Created school: {school.name}")
    else:
        print(f"⚠️ School already exists: {school.name}")

    # Create Classes
    classes = []
    for i in range(1, 11):
        class_obj, created = Class.objects.get_or_create(
            name=f"Class {i}",
            section="A"
        )
        classes.append(class_obj)
        if created:
            print(f"✅ Created: {class_obj}")
        else:
            print(f"⚠️ Already exists: {class_obj}")

    # Create Teachers
    teachers_data = [
        {'username': 'math_teacher', 'subject': 'Mathematics', 'first_name': 'John', 'last_name': 'Smith'},
        {'username': 'science_teacher', 'subject': 'Science', 'first_name': 'Sarah', 'last_name': 'Johnson'},
        {'username': 'english_teacher', 'subject': 'English', 'first_name': 'Emily', 'last_name': 'Brown'},
        {'username': 'history_teacher', 'subject': 'History', 'first_name': 'Michael', 'last_name': 'Davis'},
        {'username': 'physics_teacher', 'subject': 'Physics', 'first_name': 'Robert', 'last_name': 'Wilson'},
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

    # Create Sample Students
    students_data = [
        {'username': 'student1', 'first_name': 'Alice', 'last_name': 'Johnson', 'class_name': 'Class 10'},
        {'username': 'student2', 'first_name': 'Bob', 'last_name': 'Smith', 'class_name': 'Class 9'},
        {'username': 'student3', 'first_name': 'Carol', 'last_name': 'Williams', 'class_name': 'Class 8'},
    ]

    for i, data in enumerate(students_data, 1):
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': f'{data["username"]}@school.com',
                'user_type': 'student',
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✅ Created user: {user.username}")

        student, created = Student.objects.get_or_create(
            user=user,
            defaults={
                'student_id': f'STU{i:06d}',
                'class_name': data['class_name'],
                'section': 'A',
                'roll_number': i
            }
        )
        if created:
            print(f"✅ Created student: {student.user.get_full_name()} - {student.student_id}")
        else:
            print(f"⚠️ Student already exists: {student.user.get_full_name()}")

    # Create Sample Notices
    notices_data = [
        {
            'title': 'Welcome Back to School',
            'content': 'We are excited to welcome all students and teachers back for the new academic year. Classes will begin on Monday.',
            'target_audience': 'All'
        },
        {
            'title': 'Parent-Teacher Meeting',
            'content': 'There will be a parent-teacher meeting this Friday at 2:00 PM in the school auditorium.',
            'target_audience': 'All'
        },
        {
            'title': 'Science Fair Competition',
            'content': 'Annual science fair competition will be held next month. Interested students should register with their science teachers.',
            'target_audience': 'Students'
        },
    ]

    for notice_data in notices_data:
        notice, created = Notice.objects.get_or_create(
            title=notice_data['title'],
            defaults=notice_data
        )
        if created:
            print(f"✅ Created notice: {notice.title}")
        else:
            print(f"⚠️ Notice already exists: {notice.title}")

    print("\n🎉 Sample data creation completed!")
    print("You can now login with:")
    print("👨‍🏫 Teacher: username='math_teacher', password='password123'")
    print("👨‍🎓 Student: username='student1', password='password123'")
    print("🔑 Admin: Create using 'python manage.py createsuperuser'")


if __name__ == '__main__':
    create_sample_data()