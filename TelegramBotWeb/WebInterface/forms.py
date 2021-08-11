from django import forms
from .models import Employee, Group

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)



class MessSender(forms.Form):
    persons = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(),required=False, widget=forms.SelectMultiple,label="Пользователи")
    group = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),required=False, widget=forms.CheckboxSelectMultiple,label="Группы")
    
    text_choice = forms.CharField(widget=forms.Textarea, label="Выбранные значения")
    

# class BotStatus(forms.Form):
#     status = forms.BooleanField(label="Статус бота")
#     text = forms.TextField(label="Текст сообщений")
    