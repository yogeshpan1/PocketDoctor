from django.urls import path
from .views import doctor_dashboard, appointment_detail, write_prescription, view_prescription

app_name = 'doctors'

urlpatterns = [
    path('', doctor_dashboard, name='dashboard'),
    path('appointment/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
    path('appointment/<int:appointment_id>/prescription/write/', write_prescription, name='write_prescription'),
    path('appointment/<int:appointment_id>/prescription/', view_prescription, name='view_prescription'),
]