from django import forms
from .models import Student, Teacher, Notice, Attendance, Result, Fee, Book, BookIssue, ClassRoutine, Class, Subject, \
    Gallery  # Gallery import করুন


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
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter notice title'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Enter notice content'}),
            'target_audience': forms.Select(attrs={'class': 'form-select'}),
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


class SelectWithInput(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices)
        if attrs:
            attrs['class'] = attrs.get('class', '') + ' select-with-input'
        else:
            self.attrs = {'class': 'select-with-input'}


class ClassRoutineForm(forms.ModelForm):
    new_subject = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Or enter new subject name',
            'style': 'display: none; margin-top: 5px;'
        }),
        label="New Subject"
    )

    class Meta:
        model = ClassRoutine
        fields = ['class_name', 'day', 'subject', 'start_time', 'end_time']
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'day': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'subject': SelectWithInput(attrs={'class': 'form-select', 'required': 'required'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': 'required'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_name'].required = True
        self.fields['day'].required = True
        self.fields['subject'].required = False
        self.fields['start_time'].required = True
        self.fields['end_time'].required = True

        self.fields['subject'].empty_label = "--- Select existing subject or add new below ---"

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        subject = cleaned_data.get('subject')
        new_subject = cleaned_data.get('new_subject')
        class_name = cleaned_data.get('class_name')

        if not subject and not new_subject:
            raise forms.ValidationError("Please either select an existing subject or enter a new subject name.")

        if new_subject and not subject:
            from django.contrib.auth.models import User
            user = self.get_user()
            if user and user.user_type == 'teacher':
                try:
                    teacher = Teacher.objects.get(user=user)
                    subject, created = Subject.objects.get_or_create(
                        name=new_subject,
                        class_name=class_name,
                        teacher=teacher,
                        defaults={}
                    )
                    cleaned_data['subject'] = subject
                    self.cleaned_data['subject'] = subject
                except Teacher.DoesNotExist:
                    raise forms.ValidationError("Teacher profile not found.")
            else:
                raise forms.ValidationError("Only teachers can create new subjects.")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data

    def get_user(self):
        if hasattr(self, 'user'):
            return self.user
        return None

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


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