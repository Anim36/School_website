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

    # Address fields for all users
    division = forms.ChoiceField(
        choices=[
            ('', 'Select Division'),
            ('Dhaka', 'Dhaka Division'),
            ('Chittagong', 'Chittagong Division'),
            ('Rajshahi', 'Rajshahi Division'),
            ('Khulna', 'Khulna Division'),
            ('Barisal', 'Barisal Division'),
            ('Sylhet', 'Sylhet Division'),
            ('Rangpur', 'Rangpur Division'),
            ('Mymensingh', 'Mymensingh Division'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    district = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Narail, Jashore, Dhaka'})
    )
    thana = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Narail Sadar, Lohagara, Kalia'})
    )
    postal_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 7500'})
    )
    area_village = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Village Name'})
    )
    house_details = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House No:'})
    )

    # Student specific fields - FIXED: Make them required=False initially
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
    father_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter father\'s name'})
    )
    mother_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mother\'s name'})
    )
    parent_phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter parent\'s phone'})
    )
    parent_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter parent\'s email'})
    )
    parent_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter parent\'s address'})
    )

    # Teacher specific fields - FIXED: Make them required=False initially
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
    joining_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Teacher's joining date"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2',
                  'first_name', 'last_name', 'phone',
                  'division', 'district', 'thana', 'postal_code', 'area_village', 'house_details',
                  'date_of_birth', 'gender', 'class_name', 'section', 'roll_number',
                  'father_name', 'mother_name', 'parent_phone', 'parent_email', 'parent_address',
                  'teacher_gender', 'teacher_dob', 'qualification', 'specialization', 'joining_date']

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

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        # Student validation - FIXED: Only validate if user_type is student
        if user_type == 'student':
            required_student_fields = [
                ('class_name', 'Class is required for students.'),
                ('section', 'Section is required for students.'),
                ('roll_number', 'Roll number is required for students.'),
                ('father_name', "Father's name is required for students."),
                ('gender', 'Gender is required for students.'),
                ('date_of_birth', 'Date of birth is required for students.')
            ]

            for field, error_message in required_student_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, error_message)

        # Teacher validation - FIXED: Only validate if user_type is teacher
        if user_type == 'teacher':
            required_teacher_fields = [
                ('qualification', 'Qualification is required for teachers.'),
                ('specialization', 'Specialization is required for teachers.'),
                ('teacher_gender', 'Gender is required for teachers.'),
                ('teacher_dob', 'Date of birth is required for teachers.'),
                ('joining_date', 'Joining date is required for teachers.')
            ]

            for field, error_message in required_teacher_fields:
                field_value = cleaned_data.get(field)
                if not field_value:
                    self.add_error(field, error_message)
                elif isinstance(field_value, str) and field_value.strip() == '':
                    self.add_error(field, error_message)

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