from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'student'

urlpatterns = [
    path('student-home/', views.student, name='student-home'),
    path('student_profile/', views.studentProfile, name='student-profile'),
    path('student-courses/', views.studentCourses, name='student-courses'),
    path('student-enroll', views.enroll, name='student-enroll'),
    path('student-activities/', views.activities, name='student-activities'),
    path('student-profile-specific/<int:student_id>/', views.studentProfileSpecific, name='student-profile-specific'),
    path('student-change-credentials/<int:student_id>/', views.studentChangeCredentials, name='change-credentials'),
]
