from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, FileResponse, HttpResponse
from sharedmodels.models import Authentications, Users, Teachers, Activities, Students, Courses, Seminars, Laboratories, Activityassignments
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.core.exceptions import ValidationError
from sharedmodels.models import Admins


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
    except Authentications.DoesNotExist:
        # User does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'admin':
        # User is not an admin
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is an admin
    return render(request, 'adminDB/admin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminProfile(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
        admin = Admins.objects.get(admin__user_id=user_id)  # Fetch the admin data
    except (Authentications.DoesNotExist, Teachers.DoesNotExist):
        # User or Admin does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'admin':
        # User is not an admin
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is an admin
    context = {
        'user': user,
        'admin': admin,
    }
    return render(request, 'adminDB/admin-profile.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminViewTeachers(request, department=None):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
        admin = Admins.objects.get(admin__user_id=user_id)  # Fetch the admin data
    except (Authentications.DoesNotExist, Admins.DoesNotExist):
        # User or Admin does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'admin':
        # User is not an admin
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is an admin
    if department:
        # Fetch only the teachers of the specified department
        teachers = Teachers.objects.filter(teacher_department=department).order_by('teacher_department')
    else:
        # Fetch all teachers
        teachers = Teachers.objects.all().order_by('teacher_department')
    context = {
        'user': user,
        'admin': admin,
        'teachers': teachers,
    }
    return render(request, 'adminDB/admin-view-teachers.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminViewStudents(request, studyYear = 0):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
        admin = Admins.objects.get(admin__user_id=user_id)  # Fetch the admin data
    except (Authentications.DoesNotExist, Admins.DoesNotExist):
        # User or Admin does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'admin':
        # User is not an admin
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is an admin
    if studyYear:
        # Fetch only the students of the specified study year
        students = Students.objects.filter(student_study_year=studyYear).order_by('student_study_year')
    else:
        # Fetch all students
        students = Students.objects.all().order_by('student_study_year')
    context = {
        'user': user,
        'admin': admin,
        'students': students,
    }
    return render(request, 'adminDB/admin-view-students.html', context)