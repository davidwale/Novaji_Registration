from django.db import models
import bcrypt
from datetime import datetime, timedelta
from django.core.validators import EmailValidator, RegexValidator

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=11, 
        validators=[RegexValidator(r'^\d{11}$', message="Phone number must be 11 digits")]
    )
    email = models.EmailField(
        validators=[
            EmailValidator(message="Must be a valid Gmail, Yahoo, or Outlook email")
        ]
    )
    password = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()
        super().save(*args, **kwargs)
