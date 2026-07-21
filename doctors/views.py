from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from appointments.models import Appointment, Message, Prescription


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


@doctor_required
def appointment_detail(request, appointment_id):
    doctor = request.user.doctor_profile
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    if request.method == 'POST':
        if 'send_message' in request.POST:
            body = request.POST.get('body', '').strip()
            if body:
                Message.objects.create(appointment=appointment, sender=request.user, body=body)
                messages.success(request, 'Message sent.')
            return redirect('doctors:appointment_detail', appointment_id=appointment.id)

        if 'update_status' in request.POST:
            new_status = request.POST.get('status')
            valid_statuses = dict(Appointment.STATUS_CHOICES)
            if new_status in valid_statuses:
                appointment.status = new_status
                appointment.save()
                messages.success(request, f'Status updated to {valid_statuses[new_status]}.')
            return redirect('doctors:appointment_detail', appointment_id=appointment.id)

    thread = appointment.messages.all()
    has_prescription = hasattr(appointment, 'prescription')

    return render(request, 'doctors/appointment_detail.html', {
        'doctor': doctor,
        'appointment': appointment,
        'thread': thread,
        'has_prescription': has_prescription,
    })


@doctor_required
def write_prescription(request, appointment_id):
    doctor = request.user.doctor_profile
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    # If one already exists, edit it instead of creating a duplicate
    prescription = getattr(appointment, 'prescription', None)

    if request.method == 'POST':
        medicines = request.POST.get('medicines', '').strip()
        notes = request.POST.get('notes', '').strip()

        if not medicines:
            messages.error(request, 'Please list at least one medicine.')
        else:
            if prescription:
                prescription.medicines = medicines
                prescription.notes = notes
                prescription.save()
                messages.success(request, 'Prescription updated.')
            else:
                Prescription.objects.create(appointment=appointment, medicines=medicines, notes=notes)
                messages.success(request, 'Prescription created.')
            return redirect('doctors:view_prescription', appointment_id=appointment.id)

    return render(request, 'doctors/write_prescription.html', {
        'doctor': doctor,
        'appointment': appointment,
        'prescription': prescription,
    })


@doctor_required
def view_prescription(request, appointment_id):
    doctor = request.user.doctor_profile
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    prescription = getattr(appointment, 'prescription', None)

    if not prescription:
        messages.error(request, 'No prescription exists yet for this appointment.')
        return redirect('doctors:appointment_detail', appointment_id=appointment.id)

    return render(request, 'doctors/view_prescription.html', {
        'doctor': doctor,
        'appointment': appointment,
        'prescription': prescription,
    })