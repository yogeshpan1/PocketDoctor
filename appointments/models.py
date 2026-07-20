from django.db import models
from django.conf import settings


class Doctor(models.Model):
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

    # Links a Doctor record to a real login account.
    # Nullable because we already have Doctor rows created via admin
    # before this field existed — not every Doctor needs a login yet.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_profile'
    )

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.get_department_display()})"


class DoctorTimeSlot(models.Model):
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


class Message(models.Model):
    """A message from a doctor to a patient, tied to a specific appointment."""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} on appointment #{self.appointment_id}"


class Prescription(models.Model):
    """A prescription a doctor writes for a specific appointment."""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    medicines = models.TextField(help_text="One medicine per line, e.g. 'Paracetamol 500mg - twice daily'")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for appointment #{self.appointment_id}"