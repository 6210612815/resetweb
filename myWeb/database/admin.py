from django.contrib import admin
# Register your models here.

from .models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "personal_id","user_id")

admin.site.register(Employee, EmployeeAdmin)

