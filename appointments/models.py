from django.db import models
from django.conf import settings


class Doctor(models.Model):
    """
    A doctor profile. Kept separate from the User model —
    not every doctor needs a login account right away, and
    admins can manage doctor listings without creating users.
    """
    DEPARTMENT_CHOICES = [
        ('general', 'General Physician'),
        ('cardiology', 'Cardiologist'),
        ('dermatology', 'Dermatologist'),
        ('neurology', 'Neurologist'),
        ('gastroenterology', 'Gastroenterologist'),
        ('orthopedics', 'Orthopedic Surgeon'),
        ('pulmonology', 'Pulmonologist'),
        ('ent', 'ENT Specialist'),
        ('psychiatry', 'Psychiatrist'),
    ]

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.get_department_display()})"


class DoctorTimeSlot(models.Model):
    """A recurring weekly slot a doctor is available in."""
    DAY_CHOICES = [
        ('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'),
        ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.name} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class Appointment(models.Model):
    """A booked appointment, linked to a real User instead of a raw email string."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    problem = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} -> {self.doctor.name} on {self.date}"

    class Meta:
        ordering = ['-date', '-time']