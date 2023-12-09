from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .forms import PersonalDataForm
from django.contrib.auth import logout
from .models import PersonalData
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.encoding import force_str



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not (username and email and password):
            return render(request, 'register.html', {'error': 'All fields are required'})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})

        # # Check if email already exists
        # if User.objects.filter(email=email).exists():
        #     return render(request, 'register.html', {'error': 'Email already in use'})

        # Create user and user profile
        user = User.objects.create_user(username=username, email=email, password=password)
        profile = UserProfile.objects.create(user=user)

        # Send email with activation link
        activation_link = f"{request.build_absolute_uri('/activate/')}{profile.activation_token}"
        send_mail(
            'Aktywuj swoje konto',
            f'Kliknij w link, aby aktywować konto: {activation_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return redirect('login')

    return render(request, 'register.html')



def activate(request, token):
    try:
        profile = UserProfile.objects.get(activation_token=token)
        user = profile.user
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    except UserProfile.DoesNotExist:
        return render(request, 'activation_failed.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def home_page(request):
    return render(request, 'home.html')  # Ensure you have a 'home.html' template


def register_page(request):
    return render(request, 'register.html')  # Ensure you have a 'home.html' template

@login_required
def secret_page(request):
    return render(request, 'secret_page.html')


@login_required
def add_personal_data(request):
    if request.method == 'POST':
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            personal_data = form.save(commit=False)
            personal_data.user = request.user
            personal_data.save()
            return redirect('view_personal_data')
    else:
        form = PersonalDataForm()
    return render(request, 'add_personal_data.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def view_personal_data(request):
    user_data = PersonalData.objects.filter(user=request.user)
    return render(request, 'view_personal_data.html', {'user_data': user_data})


@login_required()
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user = request.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link = request.build_absolute_uri(f'/activate_new_password/{uid}/{token}/')
        send_mail(
            'Aktywuj swoje konto',
            f'Kliknij w link, aby aktywować nowe haslo: {link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        user.set_password(new_password)
        user.is_active = False
        user.save()
        messages.info(request, 'Please check your email to activate your new password.')
        return redirect('home')
    return render(request, 'change_password.html')

def activate_new_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.save()
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Here, set the new password for the user and save it
        user.is_active = True
        user.save()
        messages.success(request, 'Your password has been set.')
        return redirect('login')
    else:
        print("No user")
        messages.error(request, 'The link is invalid, possibly because it has already been used.')
        return redirect('home')
