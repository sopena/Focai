from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),

    path('addstudy/', views.addStudy, name='addstudy'),
    
    path('subjects/', views.subjects, name='subjects'),
    path('addsubject/', views.addSubject, name='addsubject'),
    path("delete_subject/<str:pk>/", views.deleteSubject, name="delete_subject"),
    
]
