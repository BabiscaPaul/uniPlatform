from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from sharedmodels.models import Authentications, Users
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.urls import reverse
from sharedmodels.models import Authentications, Groupmessages, Studentenrollments, Users, Teachers, Activities, \
    Students, Courses, \
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

        # Check if an enrollment already exists for the student-teacher pair
        existing_enrollment = Studentenrollments.objects.filter(teacher_id=teacher_id, student_id=user_id)

        if not existing_enrollment.exists():
            # If an enrollment does not exist, create a new one
            studentEnroll = Studentenrollments(teacher_id=teacher_id, student_id=user_id)
            studentEnroll.save()

    return redirect('student:student-courses')


def activities(request):
    isUserStudent(request)

    user_id = request.session['user_id']
    # Fetch the enrollments for the student
    enrollments = Studentenrollments.objects.filter(student__student__user_id=user_id)

    activitiesToDisplay = []

    activities = Activities.objects.all()

    # For each enrollment, get the corresponding activity
    for enrollment in enrollments:
        for activity in activities:
            # Check if the teacher who created the activity is the same as the teacher in the student's enrollment
            if activity.activity_created_by_id == enrollment.teacher_id:
                activitiesToDisplay.append(activity)

    context = {
        'activities': activitiesToDisplay
    }

    return render(request, 'student/student-activities.html', context)


def messages(request):
    user_id = request.session['user_id']
    student = Students.objects.get(student__user_id=user_id)
    user = Users.objects.get(user_id=user_id)

    if request.method == 'POST':
        messageContent = request.POST['content']
        message = Groupmessages(message_context=messageContent, student=student)
        message.save()

    # Fetch all messages
    all_messages = Groupmessages.objects.all().order_by('message_time')

    context = {
        'all_messages': all_messages,
        'user': user
    }

    return render(request, 'student/student-messages.html', context)
