# views.py
from django.shortcuts import render
from .models import Attendance

def attendance_dashboard(request):
    records = Attendance.objects.select_related('student').order_by('-date', 'time')
    return render(request, 'attendance_dashboard.html', {'records': records})



def index(request):
    return render(request,'index.html')