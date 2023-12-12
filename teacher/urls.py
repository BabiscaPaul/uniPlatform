from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'teacher'

urlpatterns = [
    path('teacher-home/', views.teacher, name='teacher-home'),
]
