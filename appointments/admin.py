from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('id', 'doctor', 'date', 'time', 'duration', 'reason', 'created_at')

    # Add filters for quick lookup
    list_filter = ('doctor', 'date', 'time')

    # Enable search functionality
    search_fields = ('doctor__username', 'reason')

    # Sort by the most recent appointments by default
    ordering = ('-created_at',)