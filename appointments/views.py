from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def doctor_list(request):
    doctors = User.objects.filter(profile__role='doctor').select_related('profile')  # get all doctors

    now = datetime.now()
    past_appointments = (
        Appointment.objects.filter(user=request.user, date__lt=now.date()) |
        Appointment.objects.filter(user=request.user, date=now.date(), time__lt=now.time())
    ).select_related('doctor__profile').order_by('-date', '-time')

    upcoming_appointments = (
        Appointment.objects.filter(user=request.user, date__gt=now.date()) |
        Appointment.objects.filter(user=request.user, date=now.date(), time__gte=now.time())
    ).select_related('doctor__profile').order_by('date', 'time')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        doctor_id = request.POST.get('doctor_id')

        if not doctor_id or not doctor_id.isdigit():
            messages.error(request, "Invalid doctor selection.")
            return redirect('appointments')

        # Get the selected doctor
        doctor = get_object_or_404(User, id=int(doctor_id), profile__role='doctor')
        form.initial['doctor'] = doctor

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.user = request.user
            appointment.save()
            messages.success(request, "Appointment successfully booked!")
            return redirect('appointments') 
        else:
            messages.error(request, "There was an error booking the appointment. Please try again.")
            return render(request, 'appointments.html', {
                'doctors': doctors,
                'form': form,
                'doctor_id': doctor_id,
                'past_appointments': past_appointments,
                'upcoming_appointments': upcoming_appointments,
            })
    else:
        form = AppointmentForm()

    return render(request, 'appointments.html', {
        'doctors': doctors,
        'form': form,
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
        'TIME_CHOICES': TIME_CHOICES,
        'DURATION_CHOICES': DURATION_CHOICES,
    })

#cancel appointment 
@login_required
def cancel_appointment(request, appointment_id):
    try:
        #checks if appointment belongs to logged in user
        appointment = Appointment.objects.get(id=appointment_id, user=request.user)
        appointment.delete() 
        messages.success(request, "Appointment has been cancelled.")
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found")
    

    return redirect('appointments')

TIME_CHOICES = [
    ("09:00", "9:00 AM"),
    ("09:30", "9:30 AM"),
    ("10:00", "10:00 AM"),
    ("10:30", "10:30 AM"),
    ("11:00", "11:00 AM"),
    ("11:30", "11:30 AM"),
    ("12:00", "12:00 PM"),
    ("12:30", "12:30 PM"),
    ("13:00", "1:00 PM"),
    ("13:30", "1:30 PM"),
    ("14:00", "2:00 PM"),
    ("14:30", "2:30 PM"),
    ("15:00", "3:00 PM"),
    ("15:30", "3:30 PM"),
    ("16:00", "4:00 PM")
]

DURATION_CHOICES = [
    (30, "30 Minutes"),
    (60, "1 Hour"),
]

@login_required
def reschedule_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        new_date = request.POST.get('date')
        new_time = request.POST.get('time')

        #validation against time choices
        valid_times = [choice[0] for choice in TIME_CHOICES]
        if new_time not in valid_times:
            messages.error(request, "Invalid time selection. Please choose a valid time.")
            return redirect('appointments')

        try:
            # Fetch the appointment
            appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

            # Validate the new datetime
            new_datetime = datetime.combine(datetime.strptime(new_date, '%Y-%m-%d').date(),
                                            datetime.strptime(new_time, '%H:%M').time())
            if new_datetime < datetime.now():
                messages.error(request, "You cannot reschedule to a past time.")
                return redirect('appointments')

            # Check for conflicts
            overlapping_appointments = Appointment.objects.filter(
            doctor=appointment.doctor,
            date=new_datetime.date(),
            time__lt=(new_datetime + appointment.duration).time(),
            time__gte=new_datetime.time()
            ).exclude(id=appointment.id)
    
            if overlapping_appointments.exists():
                messages.error(request, "This time slot is not available. Please choose a different time.")
                return redirect('appointments')


            appointment.date = new_datetime.date()
            appointment.time = new_datetime.time()
            appointment.save()

            messages.success(request, "Appointment successfully rescheduled.")
            return redirect('appointments')

        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found or you do not have permission to reschedule it.")
            return redirect('appointments')
        
@login_required
def doctor_appointments_view(request):
    if request.user.profile.role != 'doctor':
        return redirect('dashboard')

    today = date.today()

    upcoming_appointments = Appointment.objects.filter(doctor=request.user, date__gte=today).order_by('date')

    past_appointments = Appointment.objects.filter(doctor=request.user, date__lt=today).order_by('-date')

    context = {
        "upcoming_appointments": upcoming_appointments,
        "past_appointments": past_appointments,
    }

    return render(request, "doctor_appointments.html", context)        