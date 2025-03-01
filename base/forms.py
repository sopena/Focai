from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, UserSubjects

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "password1", "password2"]


class AddStudyForm(ModelForm):
    class Meta:
        model = UserSubjects
        fields = '__all__'
        excludes = ['user']


class AddSubjectForm(ModelForm):
    class Meta:
        model = UserSubjects
        fields = ['subject']

    