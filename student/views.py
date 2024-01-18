from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from sharedmodels.models import Authentications, Users
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.urls import reverse
from sharedmodels.models import Authentications, Groupmembers, Studygroups, Grades, Groupmessages, Studentenrollments, \
    Users, \
    Teachers, Activities, \
    Students, Courses, \
    Seminars, Laboratories, \
    Activityassignments
from django.utils import timezone


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


def messages_1(request):
    return render(request, 'student/student-messages-1.html')


def creategroupPage(request):
    return render(request, 'student/student-creategroup.html')


def creategroup(request):
    if request.method == 'POST':
        group_name = request.POST.get('groupName')
        group_description = request.POST.get('groupDescription')
        group_password = request.POST.get('groupPassword')

        # Check if any field is empty
        if not group_name or not group_description or not group_password:
            # One or more fields are empty, return an error message
            return render(request, 'student/student-creategroup.html', {'error': 'All fields must be completed.'})

        new_group = Studygroups(group_name=group_name, group_description=group_description,
                                group_password=group_password)
        new_group_member = Groupmembers(group=new_group,
                                        student=Students.objects.get(student__user_id=request.session['user_id']))
        new_group.save()
        new_group_member.save()

    return render(request, 'student/student-creategroup.html')


def joinGroupPage(request):
    return render(request, 'student/student-joingroup.html')


def joinGroup(request):
    if request.method == 'POST':
        group_name = request.POST.get('groupName')
        group_password = request.POST.get('groupPassword')

        try:
            # Try to get the study group with the provided name and password
            studyGroup = Studygroups.objects.get(group_name=group_name, group_password=group_password)
            group_desc = Studygroups.objects.get(group_name=group_name).group_description

            # Add the student to the study group
            potential_new_group_member = Groupmembers(group=studyGroup, student=Students.objects.get(
                student__user_id=request.session['user_id']))
            if not (Groupmembers.objects.filter(group=studyGroup, student=Students.objects.get(
                    student__user_id=request.session['user_id']))).exists():
                potential_new_group_member.save()

            student = Students.objects.get(student__user_id=request.session['user_id'])
            group_members = Groupmembers.objects.filter(student=student)
            curr_group = studyGroup
            group_messages = Groupmessages.objects.filter(group=curr_group).order_by('message_time')

            context = {
                'group_name': group_name,
                'group_desc': group_desc,
                'messages': group_messages,
                'group_id': studyGroup.group_id,
            }

            # If the study group is found, redirect to the messages page
            return render(request, 'student/student-messages.html', context)
        except Studygroups.DoesNotExist:
            # If the study group is not found, return to the join group page with an error message
            return render(request, 'student/student-joingroup.html', {'error': 'Invalid group name or password.'})

    return render(request, 'student/student-joingroup.html')


def sendMessage(request, group_id):
    user_id = request.session['user_id']
    user = Users.objects.get(user_id=user_id)
    student = Students.objects.get(student__user_id=user_id)

    if request.method == 'POST':
        messageContent = request.POST['content']
        curr_group = Studygroups.objects.get(group_id=group_id)
        message = Groupmessages(group=curr_group, message_context=messageContent, student=student,
                                message_time=timezone.now())
        message.save()

    # Fetch all messages that belong to the current group
    messages = Groupmessages.objects.filter(group=curr_group).order_by('message_time')

    context = {
        'messages': messages,
        'user': user,
        'group_id': group_id,
        'group_name': curr_group.group_name,
        'group_desc': curr_group.group_description,
    }

    return render(request, 'student/student-messages.html', context)


def grades(request):
    user_id = request.session['user_id']
    student = Students.objects.get(student__user_id=user_id)
    grades = Grades.objects.filter(student_id=student.student_id)

    context = {
        'grades': grades,
    }

    return render(request, 'student/student-grades.html', context)
