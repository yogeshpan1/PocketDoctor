from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Doctor, Appointment, Message


@login_required
def book_appointment(request):
    if hasattr(request.user, 'doctor_profile') and request.user.doctor_profile is not None:
        messages.error(request, "Doctor accounts can't book appointments.")
        return redirect('doctors:dashboard')

    department = request.GET.get('department')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointments:my_appointments')
    else:
        form = AppointmentForm()
        if department:
            matching_doctors = Doctor.objects.filter(department__icontains=department.split()[0])
            if matching_doctors.exists():
                form.fields['doctor'].queryset = matching_doctors

    return render(request, 'appointments/book.html', {'form': form})


@login_required
def my_appointments(request):
    if hasattr(request.user, 'doctor_profile') and request.user.doctor_profile is not None:
        messages.error(request, "Doctor accounts don't have patient appointments.")
        return redirect('doctors:dashboard')

    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
def appointment_detail(request, appointment_id):
    # get_object_or_404 with patient=request.user ensures a patient
    # can only ever view their own appointments, not anyone else's
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Message.objects.create(appointment=appointment, sender=request.user, body=body)
            messages.success(request, 'Message sent.')
        return redirect('appointments:appointment_detail', appointment_id=appointment.id)

    thread = appointment.messages.all()
    prescription = getattr(appointment, 'prescription', None)

    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment,
        'thread': thread,
        'prescription': prescription,
    })