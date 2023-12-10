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


# Create your views here.

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def home(request):
    return render(request, 'accounts/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        passwordConfirm = request.POST['passwordConfirm']
        role = request.POST['role']

        try:
            myusers = Users(
                user_pic=generate_random_string(20),
                user_first_name=fname,
                user_last_name=lname,
                user_address='c',
                user_phone_number=generate_random_string(20),
                user_email=email,
                user_iban=generate_random_string(30),
                user_type=role,
                user_contract_number=random.randint(1, 1000000),
            )
            print(myusers)
            myusers.full_clean()
            myusers.save()

            myauth = Authentications(
                user=myusers,
                authentication_username=username,
                authentication_password=password,
            )
            print(myauth)
            myauth.full_clean()
            myauth.save()
        except ValidationError as e:
            print(f"Validation error: {e}")
            messages.error(request, f"Error when validating data: {e}")
            return render(request, 'accounts/signup.html')
        except Exception as e:
            print(f"Error when saving Users or Authentications instance: {e}")
            traceback.print_exc()
            messages.error(request, f"Error when saving Users or Authentications instance: {e}")
            return render(request, 'accounts/signup.html')

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
        except ObjectDoesNotExist:
            user = None

        if user is not None:
            request.session['user_id'] = user.user_id  # log the user in
            messages.success(request, "You have successfully logged in")

            # check if user == student
            role = user.user_type
            if role == 'student':
                return render(request, 'student/student.html')
            elif role == 'teacher':
                return render(request, 'teacher/teacher.html')

            return render(request, 'accounts/index.html')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return render(request, 'accounts/signin.html')

    return render(request, 'accounts/signin.html')


def signout(request):
    request.session.flush()
    return redirect('accounts:signin')