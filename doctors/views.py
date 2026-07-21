from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from appointments.models import Appointment


def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'doctor_profile') or request.user.doctor_profile is None:
            messages.error(request, "You don't have access to the doctor portal.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@doctor_required
def doctor_dashboard(request):
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date', '-time')

    today = timezone.now().date()
    appointments_today = appointments.filter(date=today).count()
    pending_count = appointments.filter(status='pending').count()

    return render(request, 'doctors/dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
        'appointments_today': appointments_today,
        'pending_count': pending_count,
    })