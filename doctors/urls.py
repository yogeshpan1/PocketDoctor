from django.urls import path
from .views import doctor_dashboard

app_name = 'doctors'

urlpatterns = [
    path('', doctor_dashboard, name='dashboard'),
]