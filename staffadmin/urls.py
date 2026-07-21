from django.urls import path
from .views import admin_dashboard, manage_doctors, toggle_doctor_active

app_name = 'staffadmin'

urlpatterns = [
    path('', admin_dashboard, name='dashboard'),
    path('doctors/', manage_doctors, name='manage_doctors'),
    path('doctors/<int:doctor_id>/toggle/', toggle_doctor_active, name='toggle_doctor_active'),
]