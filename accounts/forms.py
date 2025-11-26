from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('teacher', 'Teacher')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Student specific fields
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Student's date of birth"
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Class 1, Class 2, etc.'}),
        help_text="e.g., Class 1, Class 2, etc."
    )
    section = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., A, B, C, etc.'}),
        help_text="e.g., A, B, C, etc."
    )
    roll_number = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1', 'min': '1'})
    )
    father_name = forms.CharField(  # Changed from parent_name to father_name
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter father\'s name'})
    )
    mother_name = forms.CharField(  # Added mother_name field
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mother\'s name'})
    )
    parent_phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter parent\'s phone'})
    )
    parent_email = forms.EmailField(  # Added parent_email field
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter parent\'s email'})
    )
    parent_address = forms.CharField(  # Added parent_address field
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter parent\'s address'})
    )

    # Teacher specific fields - ADD THESE
    teacher_gender = forms.ChoiceField(
        choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    teacher_dob = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Teacher's date of birth"
    )
    qualification = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., M.A., B.Ed., etc.'})
    )
    specialization = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mathematics, Science, etc.'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2',
                  'first_name', 'last_name', 'phone', 'address',  # Added address
                  'date_of_birth', 'gender', 'class_name', 'section', 'roll_number',
                  'father_name', 'mother_name', 'parent_phone', 'parent_email', 'parent_address',
                  'teacher_gender', 'teacher_dob', 'qualification', 'specialization']  # Added teacher fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['password1', 'password2']:
                if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                    if 'class' not in field.widget.attrs:
                        if isinstance(field.widget, forms.Select):
                            field.widget.attrs['class'] = 'form-select'
                        else:
                            field.widget.attrs['class'] = 'form-control'

        # Make address field optional but available for all users
        self.fields['address'] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your residential address'
            })
        )

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        # Student validation
        if user_type == 'student':
            if not cleaned_data.get('class_name'):
                self.add_error('class_name', 'Class is required for students.')
            if not cleaned_data.get('section'):
                self.add_error('section', 'Section is required for students.')
            if not cleaned_data.get('roll_number'):
                self.add_error('roll_number', 'Roll number is required for students.')
            if not cleaned_data.get('father_name'):
                self.add_error('father_name', "Father's name is required for students.")

        # Teacher validation
        if user_type == 'teacher':
            if not cleaned_data.get('qualification'):
                self.add_error('qualification', 'Qualification is required for teachers.')
            if not cleaned_data.get('specialization'):
                self.add_error('specialization', 'Specialization is required for teachers.')
            if not cleaned_data.get('teacher_gender'):
                self.add_error('teacher_gender', 'Gender is required for teachers.')

        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True


# Separate form for student registration (optional - you can remove this if using the main form)
class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Student Information
    class_name = forms.ChoiceField(
        choices=[
            ('Class 1', 'Class 1'),
            ('Class 2', 'Class 2'),
            ('Class 3', 'Class 3'),
            ('Class 4', 'Class 4'),
            ('Class 5', 'Class 5'),
            ('Class 6', 'Class 6'),
            ('Class 7', 'Class 7'),
            ('Class 8', 'Class 8'),
            ('Class 9', 'Class 9'),
            ('Class 10', 'Class 10'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    section = forms.ChoiceField(
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    roll_number = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter roll number'})
    )

    # Parent Information
    father_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Father's full name"
        })
    )
    mother_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Mother's full name"
        })
    )
    parent_phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Parent's phone number"
        })
    )
    parent_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "Parent's email address"
        })
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'phone',
            'class_name', 'section', 'roll_number',
            'father_name', 'mother_name', 'parent_phone', 'parent_email'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'}),
        }