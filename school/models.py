from django.db import models
from accounts.models import User


class SchoolInfo(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='school_logo/')
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)  # Optional করা হয়েছে
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    class_name = models.CharField(max_length=50, default='Class 1')
    section = models.CharField(max_length=10, default='A')
    roll_number = models.IntegerField(default=1)
    parent_name = models.CharField(max_length=100, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)
    admission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)  # Make optional
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    qualification = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField(auto_now_add=True)  # Auto set
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Class(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} - {self.section}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ClassRoutine(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=(
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_name} - {self.day}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    target_audience = models.CharField(max_length=20, choices=(
        ('All', 'All'),
        ('Teachers', 'Teachers'),
        ('Students', 'Students'),
        ('Parents', 'Parents'),
    ))

    def __str__(self):
        return self.title


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ))
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.student} - {self.subject}"


class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.amount}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    quantity = models.IntegerField()
    available = models.IntegerField()

    def __str__(self):
        return self.title


class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book} - {self.student}"


class Gallery(models.Model):
    CATEGORY_CHOICES = (
        ('school', 'School Campus'),
        ('events', 'School Events'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural Programs'),
        ('classroom', 'Classroom Activities'),
        ('teachers', 'Teachers'),
        ('students', 'Students'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='school')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Gallery"
        ordering = ['-upload_date']


class Contact(models.Model):
    SUBJECT_CHOICES = (
        ('admission', 'Admission Inquiry'),
        ('academic', 'Academic Information'),
        ('fee', 'Fee Structure'),
        ('general', 'General Inquiry'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject} - {self.submitted_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Contact Messages"