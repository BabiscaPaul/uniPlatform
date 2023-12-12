from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from sharedmodels.models import Authentications, Users
from django.views.decorators.cache import cache_control


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
