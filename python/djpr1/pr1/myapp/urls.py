from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.attendance_dashboard, name="attendance_dashboard"),
    path("",views.index),

]
