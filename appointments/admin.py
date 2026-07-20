from django.contrib import admin
from .models import Doctor, DoctorTimeSlot, Appointment, Message, Prescription

admin.site.register(Doctor)
admin.site.register(DoctorTimeSlot)
admin.site.register(Appointment)
admin.site.register(Message)
admin.site.register(Prescription)