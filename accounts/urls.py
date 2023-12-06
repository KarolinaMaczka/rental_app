from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uuid:token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('', views.home_page, name='home'),
    path('register_page/', views.register_page, name='register_page'),
    path('secret/', views.secret_page, name='secret_page'),
    path('add_personal_data/', views.add_personal_data, name='add_personal_data'),
    path('logout/', views.logout_view, name='logout'),
    path('view_personal_data/', views.view_personal_data, name='view_personal_data'),

]
