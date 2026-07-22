from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from appointments.models import Doctor, Appointment, Message, Prescription, DoctorTimeSlot


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


@staff_required
def add_doctor(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        department = request.POST.get('department')
        bio = request.POST.get('bio', '').strip()

        if not name or not department:
            messages.error(request, 'Name and department are required.')
        else:
            Doctor.objects.create(name=name, department=department, bio=bio)
            messages.success(request, f'Dr. {name} added successfully.')
            return redirect('staffadmin:manage_doctors')

    return render(request, 'staffadmin/add_doctor.html', {
        'department_choices': Doctor.DEPARTMENT_CHOICES,
    })


@staff_required
def manage_patients(request):
    # Exclude staff/superuser accounts from the patient list entirely —
    # admins manage staff access through Django's own auth system, not here
    patients = User.objects.filter(role='patient', is_staff=False).order_by('username')
    return render(request, 'staffadmin/manage_patients.html', {'patients': patients})


@staff_required
def toggle_patient_active(request, user_id):
    patient = get_object_or_404(User, id=user_id, role='patient', is_staff=False)
    patient.is_active = not patient.is_active
    patient.save()
    status = 'activated' if patient.is_active else 'deactivated'
    messages.success(request, f'{patient.username} has been {status}.')
    return redirect('staffadmin:manage_patients')


@staff_required
def patient_detail(request, user_id):
    patient = get_object_or_404(User, id=user_id, role='patient', is_staff=False)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')
    return render(request, 'staffadmin/patient_detail.html', {
        'patient': patient,
        'appointments': appointments,
    })

@staff_required
def doctor_timeslots(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        if 'add_slot' in request.POST:
            day = request.POST.get('day_of_week')
            start = request.POST.get('start_time')
            end = request.POST.get('end_time')
            if day and start and end:
                DoctorTimeSlot.objects.create(
                    doctor=doctor, day_of_week=day, start_time=start, end_time=end
                )
                messages.success(request, 'Time slot added.')
            else:
                messages.error(request, 'Please fill in all fields.')

        if 'delete_slot' in request.POST:
            slot_id = request.POST.get('slot_id')
            DoctorTimeSlot.objects.filter(id=slot_id, doctor=doctor).delete()
            messages.success(request, 'Time slot removed.')

        return redirect('staffadmin:doctor_timeslots', doctor_id=doctor.id)

    slots = doctor.time_slots.all().order_by('day_of_week', 'start_time')
    return render(request, 'staffadmin/doctor_timeslots.html', {
        'doctor': doctor,
        'slots': slots,
        'day_choices': DoctorTimeSlot.DAY_CHOICES,
    })