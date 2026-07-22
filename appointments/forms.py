from django import forms
from .models import Appointment, Doctor, DoctorTimeSlot
import datetime


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'problem', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'problem': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'field-input'})

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if doctor and date and time:
            day_map = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}
            day_code = day_map[date.weekday()]

            matching_slot = DoctorTimeSlot.objects.filter(
                doctor=doctor,
                day_of_week=day_code,
                is_active=True,
                start_time__lte=time,
                end_time__gte=time,
            ).exists()

            if not matching_slot:
                if not DoctorTimeSlot.objects.filter(doctor=doctor, is_active=True).exists():
                    raise forms.ValidationError(
                        f"Dr. {doctor.name} hasn't set their availability yet. Please choose another doctor or check back later."
                    )
                raise forms.ValidationError(
                    f"Dr. {doctor.name} isn't available at that day/time. Please check their availability and try again."
                )

            # Prevent double-booking the same doctor at the same exact slot
            already_booked = Appointment.objects.filter(
                doctor=doctor, date=date, time=time
            ).exclude(status='cancelled').exists()
            if already_booked:
                raise forms.ValidationError(
                    "This exact time slot is already booked. Please choose a different time."
                )

        return cleaned_data