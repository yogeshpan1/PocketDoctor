from django.contrib import admin
from .models import Doctor, DoctorTimeSlot, Appointment

admin.site.register(Doctor)
admin.site.register(DoctorTimeSlot)
admin.site.register(Appointment)