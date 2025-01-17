from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_company, name='register_company'),
    path('registration-complete/', views.registration_complete, name='registration_complete'),
]
