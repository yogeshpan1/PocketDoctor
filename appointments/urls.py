from django.urls import path
from .views import book_appointment, my_appointments

app_name = 'appointments'

urlpatterns = [
    path('book/', book_appointment, name='book'),
    path('my-appointments/', my_appointments, name='my_appointments'),
]