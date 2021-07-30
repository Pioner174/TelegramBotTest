from django.contrib import admin
from .models import Department, Locality, Employee

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Locality)
class LocalitytAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Employee)
class EmployeetAdmin(admin.ModelAdmin):
    list_display = ['user','name','surname','middle_name','position','department','locality','telephone_r','mobile_phone_r','telephone_comp','telephone_telegram']
    list_editable = ['telephone_r','mobile_phone_r','telephone_comp','telephone_telegram']
    search_fields = ('name','surname','middle_name','position','department__name','locality__name','telephone_r','mobile_phone_r','telephone_comp','telephone_telegram')
    