from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'teacher'

urlpatterns = [
    path('teacher-home/', views.teacher, name='teacher-home'),
    path('teacher-profile/', views.teacherProfile, name='teacher-profile'),
    path('teacher-activities/', views.teacherActivities, name='teacher-activities'),
    path('teacher-create-activity/', views.teacherCreateActivity, name='teacher-create-activity'),
    path('teacher-download-activities/', views.teacherDownloadActivities, name='teacher-download-activities'),
    path('teacher-students-list/', views.teacherStudentsList, name='teacher-students-list'),
    path('teacher-assign-activity/', views.teacherAssignActivity, name='teacher-assign-activity'),
    path('teacher-profile-specific/<int:teacher_id>/', views.teacherProfileSpecific, name='teacher-profile-specific'),
    path('teacher-change-credentials/<int:teacher_id>/', views.teacherChangeCredentials, name='change-credentials'),
]
