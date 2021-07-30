from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Department(models.Model):
    name = models.CharField("Название отдела", max_length=255)
    def __str__(self):
        return self.name

class Locality(models.Model):
    name = models.CharField("Населённый пункт", max_length=255)
    def __str__(self):
        return self.name
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,null=True,)
    name = models.CharField("Имя", max_length=255)
    surname = models.CharField("Фамилия",max_length=255)
    middle_name = models.CharField("Отчество", max_length=255)
    position = models.CharField("Должность", max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, verbose_name="Департамент",blank=True,null=True,)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, verbose_name="Локация",blank=True,null=True,)
    telephone_r = PhoneNumberField("Прямой телефон рабочий", blank=True)
    mobile_phone_r = PhoneNumberField("Мобильный рабочий телефон", blank=True)
    telephone_comp = PhoneNumberField("Внутренний телефон в компании", blank=True)
    telephone_telegram = PhoneNumberField("Телефон привязанный к телеге", blank=True)



