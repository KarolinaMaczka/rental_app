from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RentalForm, ReservationForm
from .models import Rental, Reservation, Image
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


@login_required
def add_rental(request):
    if request.method == 'POST':
        form = RentalForm(request.POST, request.FILES)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            rental.save()

            for file in request.FILES.getlist('images'):
                Image.objects.create(rental=rental, image=file)

            return redirect('home')
    else:
        form = RentalForm()
    return render(request, 'add_rental.html', {'form': form})


@login_required
def list_rentals(request):
    rentals = Rental.objects.filter(user=request.user)
    return render(request, 'list_rentals.html', {'rentals': rentals})


def all_rentals(request):
    rentals = Rental.objects.all()
    return render(request, 'all_rentals.html', {'rentals': rentals})

@login_required
def edit_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    if request.method == 'POST':
        form = RentalForm(request.POST, request.FILES, instance=rental)
        if form.is_valid():
            form.save()
            if request.FILES.getlist('images'):
                rental.images.all().delete()

                for file in request.FILES.getlist('images'):
                    Image.objects.create(rental=rental, image=file)

            return redirect('list_rentals')
    else:
        form = RentalForm(instance=rental)
    return render(request, 'edit_rental.html', {'form': form})


@login_required
def create_reservation(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            overlapping_reservations = Reservation.objects.filter(
                rental=rental,
                start_date__lte=end_date,
                end_date__gte=start_date
            )
            if overlapping_reservations.exists():
                messages.error(request, 'This rental is already booked for the selected dates.')
            else:
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.rental = rental
                reservation.save()
                return redirect('list_rentals')
    else:
        form = ReservationForm()
    return render(request, 'create_reservation.html', {'form': form, 'rental': rental})


def get_booked_dates(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    reservations = Reservation.objects.filter(rental=rental).values_list('start_date', 'end_date')
    booked_dates = [{'start_date': res[0], 'end_date': res[1]} for res in reservations]
    return JsonResponse({'booked_dates': booked_dates})


@login_required
def toggle_reservation_approval(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, rental__user=request.user)

    if reservation.rental.user == request.user:
        reservation.approved = not reservation.approved
        reservation.save()
        message = 'Reservation approved.' if reservation.approved else 'Reservation not approved.'
        messages.success(request, message)
    else:
        messages.error(request, 'You are not authorized to approve this reservation.')

    return redirect('list_rentals')

