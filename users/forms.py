from django import forms
from .models import User
from django.core.exceptions import ValidationError
import re
from datetime import datetime

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'date_of_birth']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'.*@gmail\.com$|.*@yahoo\.com$|.*@outlook\.com$', email):
            raise ValidationError('Email must be Gmail, Yahoo, or Outlook')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise ValidationError(
                "Password must contain at least one uppercase, one lowercase letter, one number, and one special character"
            )
        return password

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        age = (datetime.now().date() - dob).days // 365
        if age < 18:
            raise ValidationError("You must be at least 18 years old")
        return dob
