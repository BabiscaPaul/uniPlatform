from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'student'

urlpatterns = [
    path('student-home/', views.student, name='student-home'),
    path('student_profile/', views.studentProfile, name='student-profile'),
    path('student-courses/', views.studentCourses, name='student-courses'),
    path('student-enroll', views.enroll, name='student-enroll'),
]
