from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Doctor, Appointment


@login_required
def book_appointment(request):
    # Pre-fill department filter if coming from the triage page
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
            # Filter the doctor dropdown to matching department, if possible
            matching_doctors = Doctor.objects.filter(department__icontains=department.split()[0])
            if matching_doctors.exists():
                form.fields['doctor'].queryset = matching_doctors

    return render(request, 'appointments/book.html', {'form': form})


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})