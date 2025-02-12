from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from trackhealth.models import TrackHealth
import json

#Dashboard for user role
@login_required
def dashboard_view(request):
    if request.user.profile.role == 'user':
        today = date.today()
        ten_days_ago = today - timedelta(days=10)

        #gets todays tracked data and from the last 10 days
        health_data = TrackHealth.objects.filter(user=request.user, date=today).first()
        health_history = TrackHealth.objects.filter(user=request.user, date__gte=ten_days_ago).order_by('date')

        #sorted data for the barchart
        health_dates = [entry.date.strftime('%b %d') for entry in health_history]
        blood_pressure_systolic_data = [entry.blood_pressure_systolic for entry in health_history]
        blood_pressure_diastolic_data = [entry.blood_pressure_diastolic for entry in health_history]
        heart_rate_data = [entry.heart_rate for entry in health_history]
        blood_glucose_data = [entry.blood_glucose for entry in health_history]
        bmi_data = [entry.bmi for entry in health_history]
        weight_data = [entry.weight for entry in health_history]


        # Fetch appointments for today
        todays_appointments = Appointment.objects.filter(user=request.user, date=today).select_related('doctor__profile')

        #default values
        if not health_data:
            health_data = {
                "blood_pressure_systolic": 0,
                "blood_pressure_diastolic": 0,
                "heart_rate": 0,
                "weight": 0,
                "height": 0,
                "bmi": 0,
                "activity_level": "N/A",
                "blood_glucose": 0
            }

        context = {
            "health_data": health_data,
            "todays_appointments": todays_appointments,
            "health_dates": json.dumps(health_dates),
            "blood_pressure_systolic_data": json.dumps(blood_pressure_systolic_data),
            "blood_pressure_diastolic_data": json.dumps(blood_pressure_diastolic_data),
            "heart_rate_data": json.dumps(heart_rate_data),
            "blood_glucose_data": json.dumps(blood_glucose_data),
            "bmi_data": json.dumps(bmi_data),
            "weight_data": json.dumps(weight_data),
        }

        return render(request, "dashboard.html", context)

    #dashboard for doctor role
    elif request.user.profile.role == 'doctor':
        today = date.today()
    
        # Fetch appointments for doctor today
        todays_appointments = Appointment.objects.filter(doctor=request.user, date=today)

        context = {
            "todays_appointments": todays_appointments,
        }

        return render(request, "doctor_dashboard.html", context)
    #dashboard for admin
    elif request.user.profile.role == 'admin':
        return render(request, 'admin_dashboard.html')
    else:
        return redirect('login')
    

