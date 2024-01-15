from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from sharedmodels.models import Authentications, Users
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.urls import reverse
from sharedmodels.models import Authentications, Studentenrollments, Users, Teachers, Activities, Students, Courses, \
    Seminars, Laboratories, \
    Activityassignments


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
    except Authentications.DoesNotExist:
        # User does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'student':
        # User is not a student
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is a student
    return render(request, 'student/student.html')


def isUserStudent(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
        student = Students.objects.get(student__user_id=user_id)  # Fetch the student data
    except (Authentications.DoesNotExist, Students.DoesNotExist):
        # User or Student does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'student':
        # User is not a student
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is a student


def studentProfile(request):
    isUserStudent(request)

    user_id = request.session['user_id']
    student = Students.objects.get(student__user_id=user_id)

    context = {
        'student': student,
    }

    return render(request, 'student/student-profile.html', context)


def studentCourses(request):
    isUserStudent(request)

    teacher = Teachers.objects.all()

    context = {
        'teachers': teacher,
    }

    return render(request, 'student/student-courses.html', context)


def enroll(request):
    if request.method == 'POST':
        teacher_id = request.POST['teacher_id']  # Retrieve teacher_id from POST data
        user_id = request.session['user_id']  # Retrieve user_id from session data

        studentEnroll = Studentenrollments(teacher_id=teacher_id, student_id=user_id)
        studentEnroll.save()

        # Now you can use teacher_id and user_id as needed
        # ...

    return redirect('student:student-courses')


def activities(request):
    isUserStudent(request)

    user_id = request.session['user_id']
    # Fetch the enrollments for the student
    enrollments = Studentenrollments.objects.filter(student__student__user_id=user_id)
    # Fetch the courses for the enrollments
    departments = [enrollment.teacher.teacher_department for enrollment in enrollments]

    courses = Courses.objects.filter(course_name__in=departments)
    labs = Laboratories.objects.filter(laboratory_name__in=departments)
    seminars = Seminars.objects.filter(seminar_name__in=departments)

    context = {
        'courses': courses,
        'labs': labs,
        'seminars': seminars,
    }

    return render(request, 'student/student-activities.html', context)
