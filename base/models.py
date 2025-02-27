from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, password, **other_fields):
        if not email:
            raise ValueError(_("O email é obrigatório"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        return self.create_user(email, username, first_name, password, **other_fields)    

class User(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, )
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(_('email address'), unique=True, null=True)
    bio = models.TextField(_('bio'), max_length=500, null=True, blank=True)
    start_date = models.TimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    avatar = models.ImageField(null=True, default='avatar.svg')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username
    
class Subjects(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, related_name='subjects', through='UserSubjects')

    def __str__(self):
        return self.name
    

class UserSubjects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='user_subjects')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='user_subjects')
    time_studied = models.DurationField()
    last_study = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - time studied: ({}) - last study: ({})".format(self.user.username, self.subject.name, self.time_studied, self.last_study)