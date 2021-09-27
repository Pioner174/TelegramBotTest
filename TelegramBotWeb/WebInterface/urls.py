from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import *

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name="webInterface/login.html",authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="webInterface/logged_out.html"), name='logout'),
    path('mailing/', views.mailing, name='mail'),
    path('chat/', views.chat, name='chat'),
    path('update_people/',views.dynamic_people_update, name='update_people'),
]