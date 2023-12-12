# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .models import Authentications, Users
import random
import string
from django.core.exceptions import ValidationError
import traceback
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        passwordConfirm = request.POST['passwordConfirm']
        role = request.POST['role']

        myusers = Users(
            user_pic="your pic",
            user_first_name=fname,
            user_last_name=lname,
            user_address='your address',
            user_phone_number='your phone number',
            user_email=email,
            user_iban='your iban',
            user_type=role,
            user_contract_number=0
        )
        myusers.save()

        myauth = Authentications(
            user=myusers,
            authentication_username=username,
            authentication_password=password,
        )
        myauth.save()

        messages.success(request, "Your account has been successfully created")
        return redirect('accounts:signin')

    return render(request, 'accounts/signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_auth = Authentications.objects.get(authentication_username=username, authentication_password=password)
            user = user_auth.user

            if user is not None:
                request.session['user_id'] = user.user_id  # log the user in
                messages.success(request, "You have successfully logged in")

                # check if user == student
                role = user.user_type
                if role == 'student':
                    return redirect('student:student-home')
                elif role == 'teacher':
                    return redirect('teacher:teacher-home')
        except ObjectDoesNotExist:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('accounts:signin')

    return render(request, 'accounts/signin.html')


def signout(request):
    request.session.flush()
    return redirect('accounts:signin')
