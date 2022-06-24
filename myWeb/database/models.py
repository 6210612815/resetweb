from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django import forms

# Create your models here.

class Line(models.Model):
    user_id = models.CharField(max_length=50)

class Employee(models.Model):
    line = models.OneToOneField(Line,on_delete=models.CASCADE,primary_key=True,)
    employee_id = models.CharField(max_length=10)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id']
        labels = {
            'employee_id': 'รหัสพนักงาน',
        }


