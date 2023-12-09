from django.urls import path
from . import views

urlpatterns = [
    path('add_rental/', views.add_rental, name='add_rental'),
    path('list_rentals/', views.list_rentals, name='list_rentals'),
    path('edit_rental/<int:rental_id>/', views.edit_rental, name='edit_rental'),
    path('create_reservation/<int:rental_id>/', views.create_reservation, name='create_reservation'),


]