from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import LoginForm, PeopleSelect, MessSelect#, BotStatus
# from ...PythonTelegramBot.UpdaterBot import *

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, password=cd['password'], username=cd['username']) #Так тут возможно надо поменять на (request, username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Успешно аутентифицирован!')
            else:
                return HttpResponse('Ваш аккаунт отключен, обратитесь к Администратору!')
        else:
            return HttpResponse('Неверный логин или пароль!')
    else:
        form = LoginForm()
    return render(request, 'WebInterface/login.html', {'form':form})

def bot_status(request):
    pass

def mailing(request):
    if request.method == 'POST':
        malling_form = PeopleSelect(request.POST)
        if malling_form.is_valid():
            str_id=[]
            cd = malling_form.cleaned_data
            employee_tid = cd['persons'].values('t_user_id')
            for i in employee_tid:
                str_id.append(i['t_user_id'])
            for person_in_group in cd['group']:
                pass
            pass

    else:
        malling_form = PeopleSelect()
    return render(request,'WebInterface/newsletter.html', {'form': malling_form})
