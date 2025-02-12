from django import forms
from .models import TrackHealth
from django.core.exceptions import ValidationError

class HealthDataForm(forms.ModelForm):
    class Meta:
        model = TrackHealth
        fields = [
            'heart_rate', 
            'weight', 
            'height', 
            'blood_glucose', 
            'blood_pressure_systolic', 
            'blood_pressure_diastolic',
            'activity_level',  # Added activity level
            'date',
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'activity_level': forms.Select(attrs={
                'class': 'form-control',  # Add CSS class for consistent styling
            }),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        user = self.instance.user or self.initial.get('user')  # Get the user from the instance or initial data
        if TrackHealth.objects.filter(user=user, date=date).exists():
            raise ValidationError("You already have data for this date. Please select another date.")
        return date

    def clean(self):
        cleaned_data = super().clean()

        # Validation for Heart Rate
        heart_rate = cleaned_data.get('heart_rate')
        if heart_rate is not None and not (20 <= heart_rate <= 300):
            self.add_error('heart_rate', "Heart rate must be between 20 and 300 bpm.")

        # Validation for Weight
        weight = cleaned_data.get('weight')
        if weight is not None and not (10 <= weight <= 700):
            self.add_error('weight', "Weight must be between 10 and 700 kg.")

        # Validation for Height
        height = cleaned_data.get('height')
        if height is not None and not (0.5 <= height <= 3.0):
            self.add_error('height', "Height must be between 0.5 and 3.0 meters.")

        # Validation for Blood Glucose
        blood_glucose = cleaned_data.get('blood_glucose')
        if blood_glucose is not None and not (30 <= blood_glucose <= 1000):
            self.add_error('blood_glucose', "Blood glucose must be between 30 and 1000 mg/dL.")

        # Validation for Blood Pressure (Systolic)
        systolic = cleaned_data.get('blood_pressure_systolic')
        if systolic is not None and not (50 <= systolic <= 300):
            self.add_error('blood_pressure_systolic', "Systolic pressure must be between 50 and 300 mmHg.")

        # Validation for Blood Pressure (Diastolic)
        diastolic = cleaned_data.get('blood_pressure_diastolic')
        if diastolic is not None and not (30 <= diastolic <= 200):
            self.add_error('blood_pressure_diastolic', "Diastolic pressure must be between 30 and 200 mmHg.")

        return cleaned_data
