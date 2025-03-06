from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Min
from django.contrib.auth import login
from .models import User, UserSubjects, Subjects
from .forms import CustomUserCreationForm, AddStudyForm, AddSubjectForm
from utils.studies import calc_time_studied, calc_percent_asw, calendar

from datetime import date, timedelta
from django.db.models import Min

def home(request):
    
    if request.user.is_authenticated:
        hours, minutes, seconds = calc_time_studied(request)
        percent_correct_asw, correct_answers, wrong_answers = calc_percent_asw(request)

        calendar_data = calendar(request)

        context = {'hours': hours, 
                   'minutes': minutes, 
                   'percent_correct_asw': percent_correct_asw, 
                   'correct_answers': correct_answers, 
                   'wrong_answers': wrong_answers,
                   'calendar_data': calendar_data,
                   }
        
    else:
        calendar_data = None
        context = {'time_studied': 0, 'percent_correct_asw': 0, 'calendar_data': calendar_data,}

    return render(request, 'base/home.html', context)


def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    context = {}

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            context['error_user_not_exist'] = 'User does not exist'

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context['error_password_not_exist'] = 'Password does not exist'


    return render(request, 'base/login.html', context)

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

def addStudy(request):
    form = AddStudyForm()
    
    if request.method == "POST":    
        subject_id = request.POST.get('subject')
        time_studied = request.POST.get('time_studied')
        h, m, s = map(int, time_studied.split(":"))
        time_studied = timedelta(hours=h, minutes=m, seconds=s)

        UserSubjects.objects.create(
            user = request.user,
            subject = get_object_or_404(Subjects, id=subject_id),
            correct_answers = request.POST.get('correct_answers'),
            wrong_answers = request.POST.get('wrong_answers'),
            time_studied = time_studied,
            last_study = request.POST.get('last_study'),
        )
        return redirect('home')
    else:
        form = AddStudyForm()
    
    context = {'form':form}
    return render(request, 'base/addstudy.html', context)


def subjects(request):
    #user_subjects = UserSubjects.objects.filter(user_id=request.user.id)
    user_subjects = UserSubjects.objects.filter(user_id=request.user.id).values('subject').annotate(min_id=Min('id'))
    unique_subjects = UserSubjects.objects.filter(id__in=[s['min_id'] for s in user_subjects])
    context = {'user_subjects': unique_subjects}
    return render(request, 'base/subjects.html', context)

def addSubject(request):
    form = AddSubjectForm()

    if request.method == "POST":
        subject_id = request.POST.get('subject')

        UserSubjects.objects.create(
            user = request.user,
            subject = get_object_or_404(Subjects, id=subject_id),
        )
        return redirect('subjects')
    else:
        form = AddSubjectForm()
    
    context = {'form':form}
    return render(request, 'base/addsubject.html', context)


def deleteSubject(request, pk):
    if request.method == "POST":
        user = request.user
        user_subjects = UserSubjects.objects.filter(user_id=user.id, subject_id=pk).delete()
        return redirect('subjects')
    context = {}
    return render(request, 'base/delete_subject.html', context)