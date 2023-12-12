from django.shortcuts import render, redirect


# Create your views here.

def teacher(request):
    return render(request, 'teacher/teacher.html')
