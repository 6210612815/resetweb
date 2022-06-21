from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django import forms

# Create your models here.

class Line(models.Model):
    user_id = models.CharField(max_length=50)

class Employee(models.Model):
    line_id = models.OneToOneField(Line, on_delete=models.CASCADE, primary_key=True, default=None)
    employee_id = models.IntegerField()
    personal_id = models.IntegerField()

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            'employee_id': 'employee_id',
            'personal_id': 'personal_id'
        }


