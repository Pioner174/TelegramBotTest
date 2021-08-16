from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Department(models.Model):
    name = models.CharField("Название отдела", max_length=255,db_index=True)
    def __str__(self):
        return self.name

class Locality(models.Model):
    name = models.CharField("Населённый пункт", max_length=255,db_index=True)
    def __str__(self):
        return self.name    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,null=True,db_index=True)
    nickname =  models.CharField("Ник нейм в телеграмме", max_length=255, blank=True, db_index=True, null=True)
    t_user_id = models.IntegerField("id в телеге", unique=True , db_index=True)
    name = models.CharField("Имя", max_length=255,blank=True,null=True)
    surname = models.CharField("Фамилия",max_length=255,blank=True,null=True)
    middle_name = models.CharField("Отчество", max_length=255,blank=True,null=True)
    fullname = models.CharField("ФИО", max_length=255, help_text="Значение подстовляется автоматически после сохранения",blank=True,null=True, db_index=True)
    position = models.CharField("Должность", max_length=255, blank=True,null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, verbose_name="Департамент",blank=True,null=True,)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, verbose_name="Локация",blank=True,null=True,)
    telephone_r = PhoneNumberField("Прямой телефон рабочий", blank=True, null=True , db_index=True)
    mobile_phone_r = PhoneNumberField("Мобильный рабочий телефон", blank=True ,null=True , db_index=True)
    telephone_comp = PhoneNumberField("Внутренний телефон в компании", blank=True, null=True, db_index=True)
    telephone_telegram = PhoneNumberField("Телефон привязанный к телеге", blank=True, null=True, db_index=True)
    is_delete = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        str_full = ""
        if(self.surname != None):
            str_full = self.surname + ' '
        if(self.name != None):
            str_full += self.name + ' '
        if(self.middle_name != None):
            str_full +=self.middle_name
        if(str_full not in self.fullname  and str_full != ""):
            str_full = str_full.strip()
            self.fullname = str_full
        super().save(*args, **kwargs)
    def __str__(self):
        if (self.fullname == None):
            return self.nickname
        return self.fullname     

class Group(models.Model):
    name = models.CharField("Название группы", max_length=255, db_index=True)
    members = models.ManyToManyField(Employee, through='Memberships', through_fields=('group', 'person'))
    def __str__(self):
        return self.name    

class Memberships(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
       

class Tmessages(models.Model):
    t_message_id = models.IntegerField("Id сообщения в телеграмме", blank=True, null=True, db_index=True)
    sender = models.ForeignKey(Employee , on_delete=models.CASCADE,related_name='employee_sender_id', blank=True, null=True, verbose_name="Отправитель", db_index=True)
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='employee_recipient_id', blank=True, null=True, verbose_name="Получатель", db_index=True)
    text = models.TextField("Текст сообщения", blank=True, null=True, db_index=True)
    image = models.ImageField("Картинка", upload_to='uploads/%Y/%m/%d/', blank=True)
    datetime = models.DateTimeField("Дата и время получения", auto_now_add=True, blank=True, null=True, db_index=True)
    
    
    class Meta:
        ordering = ['datetime']

    # def __str__(self):
    #     return self.t_message_id    

    