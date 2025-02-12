from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'name', 'created_at')  # Columns to display
    list_filter = ('doctor', 'created_at')  # Filters on the right side
    search_fields = ('name', 'user__username', 'doctor__username')  # Search box
