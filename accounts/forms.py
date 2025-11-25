from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
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
        widget=forms.DateInput(attrs={'type': 'date'}),
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
    parent_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter parent\'s name'})
    )
    parent_phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter parent\'s phone'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2',
                  'first_name', 'last_name', 'phone', 'date_of_birth', 'gender',
                  'class_name', 'section', 'roll_number', 'parent_name', 'parent_phone']

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
        required=False,
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
        required=False,
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