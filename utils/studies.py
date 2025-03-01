from base.models import UserSubjects
from django.db.models import Sum
from datetime import timedelta

def calc_time_studied(request):
    user_subjects = UserSubjects.objects.filter(user_id=request.user.id)
    time_studied = user_subjects.aggregate(Sum('time_studied'))['time_studied__sum']
    if time_studied:
        total_seconds = int(time_studied.total_seconds())
    else:
        total_seconds = 0
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return hours, minutes, seconds

def calc_percent_asw(request):
    user_subjects = UserSubjects.objects.filter(user_id=request.user.id)
    correct_answers = user_subjects.aggregate(Sum('correct_answers'))['correct_answers__sum']
    wrong_answers = user_subjects.aggregate(Sum('wrong_answers'))['wrong_answers__sum']
    if correct_answers and wrong_answers:
        total_answers = correct_answers + wrong_answers
        percent = int((correct_answers*100)/total_answers)
    else: 
        total_answers = 0
        percent = 0
    return percent, correct_answers, wrong_answers


def user_subjects(user):
    subjects_list = UserSubjects.objects.filter(user_id=user.id)
    return subjects_list