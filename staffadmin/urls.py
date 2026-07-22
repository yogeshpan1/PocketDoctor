from django.urls import path
from .views import (
    admin_dashboard, manage_doctors, toggle_doctor_active, add_doctor,
    manage_patients, toggle_patient_active, patient_detail, doctor_timeslots
)

app_name = 'staffadmin'

urlpatterns = [
    path('', admin_dashboard, name='dashboard'),
    path('doctors/', manage_doctors, name='manage_doctors'),
    path('doctors/add/', add_doctor, name='add_doctor'),
    path('doctors/<int:doctor_id>/toggle/', toggle_doctor_active, name='toggle_doctor_active'),
    path('doctors/<int:doctor_id>/timeslots/', doctor_timeslots, name='doctor_timeslots'),
    path('patients/', manage_patients, name='manage_patients'),
    path('patients/<int:user_id>/toggle/', toggle_patient_active, name='toggle_patient_active'),
    path('patients/<int:user_id>/', patient_detail, name='patient_detail'),
]