from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uuid:token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('', views.home_page, name='home'),
    path('register_page/', views.register_page, name='register_page'),
    path('add_personal_data/', views.add_personal_data, name='add_personal_data'),
    path('logout/', views.logout_view, name='logout'),
    path('view_personal_data/', views.view_personal_data, name='view_personal_data'),
    path('change_password/', views.change_password, name='change_password'),
    path('activate_new_password/<uidb64>/<token>/', views.activate_new_password, name='activate_new_password'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('edit-personal-data/<int:data_id>/', views.edit_personal_data, name='edit_personal_data'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

]
