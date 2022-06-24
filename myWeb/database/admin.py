from django.contrib import admin
# Register your models here.

from .models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id",)

class LineAdmin(admin.ModelAdmin):
    list_display = ("user_id",)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Line, LineAdmin)


