from django.contrib import admin
from .models import Department, Locality, Employee, Group, Memberships



# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Locality)
class LocalitytAdmin(admin.ModelAdmin):
    list_display = ['name']

class MembershipInline(admin.TabularInline):
    model = Group.members.through

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [
        MembershipInline,
    ]
    exclude = ('members',)

@admin.register(Employee)
class EmployeetAdmin(admin.ModelAdmin):
    list_display = ['nickname','user','name','surname','middle_name','position','department','locality','telephone_r','mobile_phone_r','telephone_comp','telephone_telegram']
    list_editable = ['telephone_r','mobile_phone_r','telephone_comp','telephone_telegram']
    search_fields = ('nickname','name','surname','middle_name','position','department__name','locality__name','telephone_r','mobile_phone_r','telephone_comp','telephone_telegram')
    
@admin.register(Memberships)
class MembershipsAdmin(admin.ModelAdmin):
    list_display = ['group','person']    