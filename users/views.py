from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm
from .models import User
from uuid import uuid4

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.verification_token = str(uuid4())
            user.save()

            # Send verification email
            send_mail(
                'Verify your account',
                f'Click the link to verify your account: http://127.0.0.1:8000/verify/{user.verification_token}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect('success')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def verify(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.is_verified = True
        user.verification_token = None
        user.save()
        return render(request, 'verified.html')
    except User.DoesNotExist:
        return render(request, 'invalid_token.html')
