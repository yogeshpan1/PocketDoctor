from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from appointments.models import Doctor, Appointment, Message, Prescription


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "You don't have access to the admin dashboard.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@staff_required
def admin_dashboard(request):
    total_patients = User.objects.filter(role='patient').count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    recent_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:8]

    return render(request, 'staffadmin/dashboard.html', {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'recent_appointments': recent_appointments,
    })


@staff_required
def manage_doctors(request):
    doctors = Doctor.objects.all().order_by('name')
    return render(request, 'staffadmin/manage_doctors.html', {'doctors': doctors})


@staff_required
def toggle_doctor_active(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.is_active = not doctor.is_active
    doctor.save()
    status = 'activated' if doctor.is_active else 'deactivated'
    messages.success(request, f'Dr. {doctor.name} has been {status}.')
    return redirect('staffadmin:manage_doctors')