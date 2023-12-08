from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    return render(request, 'auth/index.html')


def signup(request):
    if (request.method == "POST"):
        username = request.POST['username']
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        passwordConfirm = request.POST['passwordConfirm']
        role = request.POST['role']

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been successfully created")

        return redirect('signin')

    return render(request, 'auth/signup.html')


def signin(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('signin')

    return render(request, 'auth/signin.html')


def signout(request):
    pass
