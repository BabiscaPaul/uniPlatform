from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'adminDB'

urlpatterns = [
    path('admin-home/', views.admin, name='admin-home'),
    path('admin-profile/', views.adminProfile, name='admin-profile'),
    path('admin-view-teachers/<str:department>/', views.adminViewTeachers, name='admin-view-teachers-department'),
    path('admin-view-teachers/', views.adminViewTeachers, name='admin-view-teachers'),
    path('admin-view-students/<int:studyYear>/', views.adminViewStudents, name='admin-view-students-year'),
    path('admin-view-students/', views.adminViewStudents, name='admin-view-students'),
]