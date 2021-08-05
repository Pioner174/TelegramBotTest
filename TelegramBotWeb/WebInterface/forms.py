from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


# class BotStatus(forms.Form):
#     status = forms.BooleanField(label="Статус бота")
#     text = forms.TextField(label="Текст сообщений")
    