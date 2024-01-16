from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, FileResponse, HttpResponse
from sharedmodels.models import Authentications, Users, Teachers, Activities, Students, Courses, Seminars, Laboratories, Activityassignments
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import ActivityForm, TeacherForm
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.core.exceptions import ValidationError

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacher(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
    except Authentications.DoesNotExist:
        # User does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'teacher':
        # User is not a student
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is a student
    return render(request, 'teacher/teacher.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacherProfile(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
        teacher = Teachers.objects.get(teacher__user_id=user_id)  # Fetch the teacher data
    except (Authentications.DoesNotExist, Teachers.DoesNotExist):
        # User or Teacher does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'teacher':
        # User is not a teacher
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is a teacher

    assignments = Activityassignments.objects.filter(teacher=teacher)

    # Create a list of activity names
    activity_names = []
    for assignment in assignments:
        if assignment.course:
            activity_names.append(str(assignment.course.course_name))
        if assignment.laboratory:
            activity_names.append(str(assignment.laboratory.laboratory_name))
        if assignment.seminar:
            activity_names.append(str(assignment.seminar.seminar_name))

    # Join the activity names into a string
    activities = ', '.join(activity_names)

    context = {
        'teacher': teacher,
        'activities': activities,
    }

    return render(request, 'teacher/teacher-profile.html', context) 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacherProfileSpecific(request, teacher_id):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')

    try:
        teacher = Teachers.objects.get(teacher__user_id=teacher_id)  # Fetch the teacher data
    except Teachers.DoesNotExist:
        # Teacher does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")

    assignments = Activityassignments.objects.filter(teacher=teacher)

    # Create a list of activity names
    activity_names = []
    for assignment in assignments:
        if assignment.course:
            activity_names.append(str(assignment.course.course_name))
        if assignment.laboratory:
            activity_names.append(str(assignment.laboratory.laboratory_name))
        if assignment.seminar:
            activity_names.append(str(assignment.seminar.seminar_name))

    # Join the activity names into a string
    activities = ', '.join(activity_names)

    context = {'teacher': teacher, 'activities': activities}
    return render(request, 'teacher/teacher-profile.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacherActivities(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
    except Authentications.DoesNotExist:
        # User does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'teacher':
        # User is not a teacher
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is a teacher
    activities = Activities.objects.all().order_by('activity_start_date')
    return render(request, 'teacher/teacher-activities.html', {'activities': activities})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacherCreateActivity(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
    except Authentications.DoesNotExist:
        # User does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'teacher':
        # User is not a teacher
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is a teacher
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.activity_created_by = user
            activity.activity_number_of_students = 0
            activity.save()
            return redirect('teacher:teacher-activities')
    else:
        form = ActivityForm()
    return render(request, 'teacher/teacher-create-activity.html', {'form': form})

from reportlab.platypus import Spacer

def teacherDownloadActivities(request):
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Get all activities
    activities = Activities.objects.all().order_by('activity_start_date')

    # Draw the activities on the PDF.
    for activity in activities:
        text = f"Activity: {activity.activity_type}, Start Date: {activity.activity_start_date}, End Date: {activity.activity_end_date}"
        story.append(Paragraph(text, styles['Normal']))
        text = f"Created By: {activity.activity_created_by.user_first_name} {activity.activity_created_by.user_last_name}"
        story.append(Paragraph(text, styles['Normal']))
        story.append(Spacer(1, 12))  # Add a blank line after each activity

    # Build the PDF
    doc.build(story)

    # Reset the buffer's position to the start of the data.
    buffer.seek(0)

    # Create a response with the PDF data, the appropriate content type, and headers.
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="activities.pdf"'

    return response

#TODO
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacherStudentsList(request):
    if 'user_id' not in request.session:
        # User is not logged in
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
    except Authentications.DoesNotExist:
        # User does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'teacher':
        # User is not a teacher
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is a teacher
    students = Students.objects.all()
    return render(request, 'teacher/teacher-list.html', {'students': students})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacherAssignActivity(request):
    if 'user_id' not in request.session:
        return redirect('accounts:signin')
    user_id = request.session['user_id']
    try:
        user = Authentications.objects.get(user__user_id=user_id).user
    except Authentications.DoesNotExist:
        # User does not exist
        return HttpResponseForbidden("You are not authorized to view this page.")
    if user.user_type != 'teacher':
        # User is not a teacher
        return HttpResponseForbidden("You are not authorized to view this page.")
    # User is logged in and is a teacher
    teacher = Teachers.objects.get(teacher_id=user_id)

    # Get the teacher's department
    department = teacher.teacher_department

    # Check if the teacher has already assigned activities
    if Activityassignments.objects.filter(teacher=teacher).exists():
        # Redirect to profile page if activities have already been assigned
        return redirect('teacher:teacher-profile')

    # Get all available activities for this department
    available_courses = Courses.objects.filter(course_name__icontains=department)
    available_laboratories = Laboratories.objects.filter(laboratory_name__icontains=department)
    available_seminars = Seminars.objects.filter(seminar_name__icontains=department)

    if request.method == 'POST':
        selected_courses = request.POST.getlist('course')
        selected_laboratories = request.POST.getlist('laboratory')
        selected_seminars = request.POST.getlist('seminar')

        course_weight = str(request.POST.get('course_weight', '0'))
        laboratory_weight = str(request.POST.get('laboratory_weight', '0'))
        seminar_weight = str(request.POST.get('seminar_weight', '0'))

        if selected_courses and (not course_weight.isdigit() or int(course_weight) < 0):
            return redirect('teacher:teacher-assign-activity')
        if selected_laboratories and (not laboratory_weight.isdigit() or int(laboratory_weight) < 0):
            return redirect('teacher:teacher-assign-activity')
        if selected_seminars and (not seminar_weight.isdigit() or int(seminar_weight) < 0):
            return redirect('teacher:teacher-assign-activity')

        total_activities = len(selected_courses) + len(selected_laboratories) + len(selected_seminars)

        if not teacher.teacher_min_hours <= total_activities <= teacher.teacher_max_hours:
            return redirect('teacher:teacher-assign-activity')

        course_id = selected_courses[0] if selected_courses else None
        laboratory_id = selected_laboratories[0] if selected_laboratories else None
        seminar_id = selected_seminars[0] if selected_seminars else None

        course_weight = int(course_weight) if course_weight.isdigit() else None
        laboratory_weight = int(laboratory_weight) if laboratory_weight.isdigit() else None
        seminar_weight = int(seminar_weight) if seminar_weight.isdigit() else None

        # Create a single Activityassignments row with the selected IDs
        Activityassignments.objects.create(
            teacher=teacher, 
            course_id=course_id, 
            laboratory_id=laboratory_id, 
            seminar_id=seminar_id,
            course_weight=course_weight,
            laboratory_weight=laboratory_weight,
            seminar_weight=seminar_weight
        )

        # Redirect to profile page after assigning activities
        return redirect('teacher:teacher-profile')

    return render(request, 'teacher/teacher-assign-activity.html', {
        'available_courses': available_courses,
        'available_laboratories': available_laboratories,
        'available_seminars': available_seminars,
    })

def teacherChangeCredentials(request, teacher_id):
    teacher = get_object_or_404(Teachers, pk=teacher_id)
    user = teacher.teacher
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=user, teacher=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher:teacher-profile-specific', teacher_id=teacher_id)
    else:
        form = TeacherForm(instance=user, teacher=teacher)
    return render(request, 'teacher/teacher-change-credentials.html', {'form': form})