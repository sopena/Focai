from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth import login
from .models import User, UserSubjects, Subjects
from .forms import CustomUserCreationForm

def home(request):
    user_subjects = UserSubjects.objects.filter(user_id=request.user.id)
    time_studied = user_subjects.aggregate(Sum('time_studied'))['time_studied__sum']

    context = {'time_studied': time_studied}
    return render(request, 'base/home.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist")

    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, 'base/register.html', context)