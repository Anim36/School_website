from django.db import models
from accounts.models import User
from django.utils import timezone


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
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    class_name = models.CharField(max_length=50, default='Class 1')
    section = models.CharField(max_length=10, default='A')
    roll_number = models.IntegerField(default=1)

    # Parent Information
    father_name = models.CharField(max_length=100, blank=True, verbose_name="Father's Name")
    mother_name = models.CharField(max_length=100, blank=True, verbose_name="Mother's Name")
    parent_phone = models.CharField(max_length=15, blank=True, verbose_name="Parent's Phone")
    parent_email = models.EmailField(blank=True, verbose_name="Parent's Email")
    parent_address = models.TextField(blank=True, verbose_name="Parent's Address")

    division = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    thana = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    area_village = models.CharField(max_length=100, blank=True)
    house_details = models.CharField(max_length=200, blank=True)

    admission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

    def get_parent_info(self):
        """Get formatted parent information"""
        info = []
        if self.father_name:
            info.append(f"Father: {self.father_name}")
        if self.mother_name:
            info.append(f"Mother: {self.mother_name}")
        if self.parent_phone:
            info.append(f"Phone: {self.parent_phone}")
        if self.parent_email:
            info.append(f"Email: {self.parent_email}")
        return info

    def get_full_address(self):
        """সম্পূর্ণ ঠিকানা return করে"""
        address_parts = []
        if self.house_details:
            address_parts.append(self.house_details)
        if self.area_village:
            address_parts.append(self.area_village)
        if self.thana:
            address_parts.append(self.thana)
        if self.district:
            address_parts.append(self.district)
        if self.division:
            address_parts.append(self.division)
        if self.postal_code:
            address_parts.append(f"Postal Code: {self.postal_code}")

        return ", ".join(address_parts) if address_parts else "Address not provided"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    qualification = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)

    # FIXED: Remove auto_now_add=True to allow manual date selection
    joining_date = models.DateField()  # This will store the selected joining date

    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # address fields
    division = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    thana = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    area_village = models.CharField(max_length=100, blank=True)
    house_details = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_id})"

    def get_experience(self):
        """Calculate experience in years and months from the selected joining_date"""
        if self.joining_date:
            today = timezone.now().date()
            delta = today - self.joining_date

            years = delta.days // 365
            months = (delta.days % 365) // 30

            if years == 0:
                return f"{months} months"
            elif months == 0:
                return f"{years} years"
            else:
                return f"{years} years {months} months"
        return "Not specified"

    def get_full_address(self):
        """সম্পূর্ণ ঠিকানা return করে"""
        address_parts = []
        if self.house_details:
            address_parts.append(self.house_details)
        if self.area_village:
            address_parts.append(self.area_village)
        if self.thana:
            address_parts.append(self.thana)
        if self.district:
            address_parts.append(self.district)
        if self.division:
            address_parts.append(self.division)
        if self.postal_code:
            address_parts.append(f"Postal Code: {self.postal_code}")

        return ", ".join(address_parts) if address_parts else "Address not provided"


# ... rest of your models remain the same
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


class AdmissionApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    # Student Information
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    class_applying = models.CharField(max_length=50)

    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # Parent Information
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField(blank=True)

    # Educational Background
    previous_school = models.CharField(max_length=200, blank=True)
    last_class = models.CharField(max_length=50, blank=True)
    last_result = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Document Uploads
    birth_certificate = models.FileField(upload_to='admission_documents/birth_certificates/', blank=True, null=True)
    father_nid = models.FileField(upload_to='admission_documents/nid_cards/', blank=True, null=True)
    mother_nid = models.FileField(upload_to='admission_documents/nid_cards/', blank=True, null=True)
    student_photo = models.ImageField(upload_to='admission_documents/student_photos/', blank=True, null=True)
    previous_result_card = models.FileField(upload_to='admission_documents/result_cards/', blank=True, null=True)

    # Application Meta
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.class_applying} - {self.status}"

    class Meta:
        ordering = ['-application_date']
        verbose_name_plural = "Admission Applications"