from django.db import models
from django.contrib.auth.models import User

class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescribed_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')
    name = models.CharField(max_length=255)  # Prescription name
    reason = models.TextField()  # Reason for the prescription
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Prescription: {self.name} for {self.user.username}"
