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
    path('student-messages', views.messages_1, name='student-messages-1'),
    path('student-messages-creategroup', views.creategroupPage, name='student-messages-creategroup'),
    path('student-creategroup', views.creategroup, name='student-creategroup'),
    path('student-joingroup-page', views.joinGroupPage, name='student-joingroup-page'),
    path('student-joingroup', views.joinGroup, name='student-joingroup'),
    path('student-group-message/<int:group_id>/', views.sendMessage, name='student-group-messages'),
    path('student-grades', views.grades, name='student-grades'),
]
