from django import forms
from .models import (
    Student, Teacher, Notice, Attendance, Result, Fee,
    Book, BookIssue, ClassRoutine, Class, Subject,
    Gallery, Contact, AdmissionApplication, RoutinePeriod
)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ['user']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'target_audience']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter notice title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter notice content'
            }),
            'target_audience': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'class_name']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'exam_name', 'marks', 'total_marks', 'grade']


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student', 'amount', 'due_date', 'paid', 'payment_date']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'quantity', 'available']


class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = ['book', 'student', 'return_date', 'returned']


# ✅ NEW ROUTINE FORMS
class RoutinePeriodForm(forms.ModelForm):
    class Meta:
        model = RoutinePeriod
        fields = ['start_time', 'end_time', 'is_break', 'break_name', 'order']
        widgets = {
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'is_break': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'break_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Break Time, Lunch Time'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }


class ClassRoutineForm(forms.ModelForm):
    class Meta:
        model = ClassRoutine
        fields = ['class_name', 'day', 'period', 'subject', 'teacher']
        widgets = {
            'class_name': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_class_name'
            }),
            'day': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_day'
            }),
            'period': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_period'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_subject',
                'placeholder': 'Enter subject name'
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_teacher'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter periods that are not breaks
        self.fields['period'].queryset = RoutinePeriod.objects.filter(is_break=False)

        # Add empty labels
        self.fields['class_name'].empty_label = "Select Class"
        self.fields['day'].empty_label = "Select Day"
        self.fields['period'].empty_label = "Select Period"
        self.fields['subject'].empty_label = "Select Subject"
        self.fields['teacher'].empty_label = "Select Teacher"


class BulkRoutineForm(forms.Form):
    """Form for adding multiple routines at once"""
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'bulk_class_name'})
    )
    day = forms.ChoiceField(
        choices=[
            ('', 'Select Day'),
            ('Sunday', 'Sunday'),
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
        ],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'bulk_day'})
    )

    # Dynamic fields for each period
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        periods = RoutinePeriod.objects.filter(is_break=False).order_by('order')

        for period in periods:
            # ✅ Subject field text input করুন
            self.fields[f'period_{period.id}_subject'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control subject-input',
                    'data-period': period.id,
                    'placeholder': 'Enter subject name'
                })
            )
            self.fields[f'period_{period.id}_teacher'] = forms.ModelChoiceField(
                queryset=Teacher.objects.all(),
                required=False,
                widget=forms.Select(attrs={
                    'class': 'form-select teacher-select',
                    'data-period': period.id,
                    'placeholder': 'Select Teacher'
                })
            )


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter image description (optional)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number (optional)'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Your message...',
                'required': 'required'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.replace(' ', '').replace('-', '').replace('+', '').isdigit():
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'name', 'date_of_birth', 'gender', 'class_applying',
            'email', 'phone', 'address',
            'father_name', 'mother_name', 'parent_phone', 'parent_email',
            'previous_school', 'last_class', 'last_result',
            'birth_certificate', 'father_nid', 'mother_nid',
            'student_photo', 'previous_result_card'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'class_applying': forms.Select(attrs={
                'class': 'form-select'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter full address'
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter father's name"
            }),
            'mother_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter mother's name"
            }),
            'parent_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter parent's phone number"
            }),
            'parent_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter parent's email (optional)"
            }),
            'previous_school': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter previous school name (if any)'
            }),
            'last_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last class completed'
            }),
            'last_result': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter percentage',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make file fields not required in form
        self.fields['birth_certificate'].required = False
        self.fields['father_nid'].required = False
        self.fields['mother_nid'].required = False
        self.fields['student_photo'].required = False
        self.fields['previous_result_card'].required = False

        # Add Bootstrap classes to file fields
        self.fields['birth_certificate'].widget.attrs.update({'class': 'form-control'})
        self.fields['father_nid'].widget.attrs.update({'class': 'form-control'})
        self.fields['mother_nid'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_photo'].widget.attrs.update({'class': 'form-control'})
        self.fields['previous_result_card'].widget.attrs.update({'class': 'form-control'})