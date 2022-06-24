from telnetlib import KERMIT
from django.shortcuts import render, redirect
from django.contrib import messages
from database.models import Employee, EmployeeForm, Line
import requests

def index(request):
    user_id = '1234'

    # if (request.POST.get('employee_id') not in Employee.objects.get('employee_id')):
    #     messages.info(request, 'Already mapping')
    #     return redirect('index')
    if (str(user_id) in Line.objects.all()):
        a = Line.objects.get(user_id=user_id)
        # return object that connected with line_id
        employee = Employee.objects.get(line=a)
        nameEN = employee.employee_id
        data = {
            'nameEN': nameEN,
        }

        return render(request, 'greet.html', data)

    # if (str(user_id) not in Line.objects.all()):
    #     l = Line(user_id=user_id)
    #     l.save()
    #     try:
    #         Employee.objects.get(employee_id=request.POST.get('employee_id'))
    #     except Employee.DoesNotExist:
    #         if request.method == "POST":
    #             form = EmployeeForm(request.POST)
    #             if form.is_valid:
    #                 pc = Employee(
    #                     line = l,
    #                     employee_id = request.POST.get('employee_id'),
    #                 )
    #                 pc.save()
    #         else:
    #             form = EmployeeForm()

    #         return render(request, 'index.html', {'form': form})

    #     # if (Employee.objects.get(employee_id=request.POST.get('employee_id')).exist):
    #     messages.info(request, 'Already')
    #     return redirect('index')
        
    # else:    
    #     a = Line.objects.get(user_id=user_id)
    #     # return object that connected with line_id
    #     employee = Employee.objects.get(line=a)
    #     nameEN = employee.employee_id
    #     data = {
    #         'nameEN': nameEN,
    #     }

    #     return render(request, 'greet.html', data)

      # ... handle the case of that user not existing
        # if (Employee.objects.get(employee_id=request.POST.get('employee_id')).exist):
                
        #     messages.alert(request, 'Already')
        #     a = Line.objects.get(user_id=user_id)
        #     # return object that connected with line_id
        #     employee = Employee.objects.get(line=a)
        #     nameEN = employee.employee_id
        #     data = {
        #         'nameEN': nameEN,
        #     }

        #     return render(request, 'greet.html', data)
        # else:
        #     l = Line(user_id=user_id)
        #     l.save()
        #     if request.method == "POST":
        #         form = EmployeeForm(request.POST)
        #         if form.is_valid:
        #             pc = Employee(
        #                 line = l,
        #                 employee_id = request.POST.get('employee_id'),
        #             )
        #             pc.save()
        #     else:
        #         form = EmployeeForm()

        #     return render(request, 'index.html', {'form': form})
    return render(request, 'index.html')

    # try:
    #     a = Line.objects.get(user_id=user_id)
    #     # return object that connected with line_id
    #     employee = Employee.objects.get(line=a)
    #     nameEN = employee.employee_id
    #     data = {
    #         'nameEN': nameEN,
    #     }
    #     return render(request, 'greet.html', data)
    # except Line.DoesNotExist:
    #     l = Line(user_id=user_id)
    #     l.save()
    #     if request.method == "POST":
    #         form = EmployeeForm(request.POST)
    #         if form.is_valid:
    #             pc = Employee(
    #                 line = l,
    #                 employee_id = request.POST.get('employee_id'),
    #             )
    #             pc.save()
    #     else:
    #         form = EmployeeForm()
    # return render(request, 'index.html')

    # if (user_id not in Line.objects.get(user_id=user_id)):
    #     l = Line(user_id=user_id)
    #     l.save()
    #     if request.method == "POST":
    #         form = EmployeeForm(request.POST)
    #         if form.is_valid:
    #             pc = Employee(
    #                 line = l,
    #                 employee_id = request.POST.get('employee_id'),
    #             )
    #             pc.save()
    #     else:
    #         form = EmployeeForm()
    # else:
    #     # return object that connected with line_id
    #     employee = Employee.objects.get(user_id=user_id)
    #     nameEN = employee.employee_id
    #     data = {
    #         'nameEN': nameEN,
    #     }
    #     return render(request, 'greet.html', data)

    # return render(request, 'index.html')


def greet(request):
    try:
        body = {
            "UserName": "admin_ss",
            "Password": "ss123456*"
        }
        getTokenURL = 'https://p701apsi01-la02skc.azurewebsites.net/skcapi/token'
        x = requests.post(getTokenURL, json=body).json()
        myToken = x["accessToken"]
        eid = request.POST['employee_id']
        getEmpURL = f"https://p701apsi01-la01skc.azurewebsites.net/skcapi/empid/{eid}"
        auth = {"Authorization": "Bearer %s" %myToken}
        y = requests.get(getEmpURL, headers=auth).json()
        nameEN = y[0]["nameEN"]
        per_id = int(y[0]["personal_Id"])
        p_id = request.POST['personal_id']

        if int(per_id) == int(p_id):
            data = {
                'nameEN': nameEN,
            }
            form = Employee.objects.all()
            return render(request, 'greet.html', {'form': form,'nameEN': nameEN,})
        else:
            print(p_id,per_id)
            messages.info(request, 'Your Personal ID miss match')
            return redirect('index')
    except KeyError as e:
        messages.info(request, 'No Employee ID in database!')
        return redirect('index')

def reset(request):
    return render(request, 'reset.html')

def success(request):
    pass_1st = request.POST['pass_1st']
    pass_2nd = request.POST['pass_2nd']
    if pass_1st == pass_2nd:
        data = {
            'pass_1st': pass_1st,
            'pass_2nd': pass_2nd,
        }
        return render(request, 'success.html', data)
    else:
        messages.info(request, 'Your Password Not Match')
        return redirect('reset')
