from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name="webInterface/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="webInterface/logged_out.html"), name='logout'),
    path('test/', views.mailing, name='mail'),
]