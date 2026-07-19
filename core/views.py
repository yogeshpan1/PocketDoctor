from django.shortcuts import render
from appointments.models import Doctor
import random


def home_view(request):
    all_doctors = list(Doctor.objects.filter(is_active=True))
    featured_doctor = random.choice(all_doctors) if all_doctors else None
    doctors_list = all_doctors[:4]
    return render(request, 'home.html', {
        'doctors': doctors_list,
        'featured_doctor': featured_doctor,
    })