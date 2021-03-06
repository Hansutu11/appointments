from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt
import datetime
import time
today = datetime.date.today()
# Create your views here.
def index(request):
    return render(request, 'appointments/index.html')

def process(request):
    print request.POST
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errrors[error]
            messages.error(request, errrors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], email = request.POST['email'], password = hashed_pw, dob = request.POST['date'])
        request.session['id'] = user.id
    return redirect('/appointments')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        messages.success(request, "You have successfully logged in")
        return redirect('/appointments')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def logout(request):
    session.objects.all().delete()
    return render(request, '/appointments/index.html')

def appointments(request):

    context = {
        'user' : User.objects.get(id=request.session['id']),
        'date' : today,
        'appointment' : Appointment.objects.filter(date=today),
        'later_appointment' : Appointment.objects.exclude(date=today),
    }
    return render(request, "appointments/appointments.html", context)

def new_appointment(request):
    Appointment.objects.create(task=request.POST['task'], date=request.POST['date'], time=request.POST['time'], status="Pending", user_appointments=User.objects.get(id=request.session['id']))
    return redirect('/appointments')

def update(request, task_id):
    context = {
        'task' : Appointment.objects.get(id=task_id),
    }
    return render(request, "appointments/update.html", context)

def change(request, task_id):
    a = Appointment.objects.get(id=task_id)
    a.task = request.POST['task']
    a.date = request.POST['date']
    a.time = request.POST['time']
    a.status = request.POST['status']
    a.save()
    return redirect('/appointments')

def delete(request, task_id):
    Appointment.objects.get(id=task_id).delete()
    return redirect('/appointments')
