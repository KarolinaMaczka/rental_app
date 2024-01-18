from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from add_rentals.models import Reservation
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
from add_rentals.models import Reservation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        surname = request.POST['surname']

        is_valid, error_messages = validate_user_data(username, first_name, surname, email, password)
        if not is_valid:
            return render(request, 'register.html', {'errors': error_messages})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, email=email, password=password,  is_active=False)
        profile = UserProfile.objects.create(user=user, first_name=first_name, surname=surname )

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
    return render(request, 'home.html')


def register_page(request):
    return render(request, 'register.html')


@login_required
def add_personal_data(request):
    if request.method == 'POST':
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            is_valid = validate_personal_data(phone_number, address, request)
            if is_valid:
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
    user_reservations = Reservation.objects.filter(user=request.user)
    for reservation in user_reservations:
        duration = (reservation.end_date - reservation.start_date).days
        reservation.total_cost = reservation.rental.price_per_night * duration

    return render(request, 'view_personal_data.html', {
        'user_data': user_data,
        'user_reservations': user_reservations
    })


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
        user.is_active = True
        user.save()
        messages.success(request, 'Your password has been set.')
        return redirect('login')
    else:
        print("No user")
        messages.error(request, 'The link is invalid, possibly because it has already been used.')
        return redirect('home')


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if reservation.approved:
        if not any(message.message == "Approved reservations cannot be canceled." for message in messages.get_messages(request)):
            request.session['cancellation_error_reservation_id'] = reservation.id
            messages.error(request, "This reservation is already approved and cannot be canceled.")
        return redirect('view_personal_data')

    if request.method == 'POST':
        reservation.delete()
        return redirect('view_personal_data')

    return redirect('view_personal_data')


@login_required
def edit_personal_data(request, data_id):
    personal_data_instance = get_object_or_404(PersonalData, id=data_id, user=request.user)

    if request.method == 'POST':
        form = PersonalDataForm(request.POST, instance=personal_data_instance)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            is_valid = validate_personal_data(phone_number, address, request)
            if is_valid:
                form.save()
            return redirect('view_personal_data')
    else:
        form = PersonalDataForm(instance=personal_data_instance)

    return render(request, 'edit_personal_data.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
            send_mail(
                'Password Reset',
                f'Follow this link to reset your password: {link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            messages.info(request, 'Please check your email to reset your password.')
            return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this username.')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            error_messages =[]
            error_messages = validate_password(new_password, error_messages)
            is_valid = not error_messages
            if not is_valid:
                return render(request, 'forgot_password.html', {'errors': error_messages})
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset.')
            return redirect('login')
        return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('forgot_password')


def validate_user_data(username, first_name, surname, email, password):
    messages = []

    if not username.strip():
        messages.append('Username is required.')
    if not first_name.strip():
        messages.append('Name is required.')
    if not surname.strip():
        messages.append('Surname is required.')

    if not email.strip():
        messages.append('Email is required.')
    else:
        try:
            validate_email(email)
        except ValidationError:
            messages.append('Email is invalid.')

    if not password:
        messages.append('Password is required.')
    else:
        messages = validate_password(password, messages)
    is_valid = not messages

    return is_valid, messages


def validate_password(password, messages):
    if len(password) < 8:
        messages.append('Password must be at least 8 characters long.')
    if not any(char.isupper() for char in password):
        messages.append('Password must contain at least one uppercase letter.')
    if not any(char.isdigit() for char in password):
        messages.append('Password must contain at least one digit.')
    return messages

def validate_personal_data(phone_number, address, request):
    is_valid = True

    if not address.strip():
        messages.error(request, 'Address is required.')
        is_valid = False

    if not phone_number.strip():
        messages.error(request, 'Phone number is required.')
        is_valid = False
    elif not re.match(r'^\+\d{2} \d{3} \d{3} \d{3}$', phone_number):
        messages.error(request, 'Phone number is invalid. Necessary format: +xx xxx xxx xxx')
        is_valid = False

    return is_valid