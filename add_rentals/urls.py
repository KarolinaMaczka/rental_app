from django.urls import path
from . import views

urlpatterns = [
    path('add_rental/', views.add_rental, name='add_rental'),
    path('list_rentals/', views.list_rentals, name='list_rentals'),
    path('edit_rental/<int:rental_id>/', views.edit_rental, name='edit_rental'),
    path('create_reservation/<int:rental_id>/', views.create_reservation, name='create_reservation'),
    path('get_booked_dates/<int:rental_id>/', views.get_booked_dates, name='get_booked_dates'),
    path('reservation/<int:reservation_id>/toggle_approval/', views.toggle_reservation_approval, name='toggle_reservation_approval'),

]
