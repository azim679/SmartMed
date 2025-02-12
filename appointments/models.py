from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()  # Store duration as a timedelta
    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def start_time(self):
        """Return the start time of the appointment as a datetime object."""
        return datetime.combine(self.date, self.time)

    @property
    def end_time(self):
        """Calculate the end time of the appointment."""
        start = self.start_time
        return start + self.duration  # Properly calculate using the DurationField

    def __str__(self):
        return f"Appointment with {self.doctor.username} on {self.date} at {self.time}"
