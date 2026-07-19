from django.shortcuts import render
from appointments.models import Doctor


def home_view(request):
    doctors = Doctor.objects.filter(is_active=True)[:4]
    return render(request, 'home.html', {'doctors': doctors})