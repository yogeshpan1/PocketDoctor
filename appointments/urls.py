from django.urls import path
from .views import book_appointment, my_appointments, appointment_detail

app_name = 'appointments'

urlpatterns = [
    path('book/', book_appointment, name='book'),
    path('my-appointments/', my_appointments, name='my_appointments'),
    path('appointment/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
]