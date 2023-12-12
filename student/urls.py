from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'student'

urlpatterns = [
    path('student-home/', views.student, name='student-home'),
]
