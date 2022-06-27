from genericpath import exists
from telnetlib import KERMIT
from django.shortcuts import render, redirect
from django.contrib import messages
from database.models import Employee, EmployeeForm, Line
import requests


def index(request):
    user_id = '1234'

    if (Line.objects.filter(user_id=user_id).exists()):
        l = Line.objects.get(user_id=user_id)
        # check EMP ID with DB
        # if Employee.objects.filter(line=l).exists()==False:
            
        if Employee.objects.filter(line=l).exists():
            employee = Employee.objects.get(line=l)
            eid = employee.employee_id

            body = {
                "UserName": "admin_ss",
                "Password": "ss123456*"
            }
            getTokenURL = 'https://p701apsi01-la02skc.azurewebsites.net/skcapi/token'
            x = requests.post(getTokenURL, json=body).json()
            myToken = x["accessToken"]
            getEmpURL = f"https://p701apsi01-la01skc.azurewebsites.net/skcapi/empid/{eid}"
            auth = {"Authorization": "Bearer %s" %myToken}
            y = requests.get(getEmpURL, headers=auth).json()
            nameEN = y[0]["nameEN"]
            
            return render(request, 'greet.html', {'nameEN': nameEN,})
    else:
        # save LINE ID in DB
        l = Line(user_id=user_id)
        
        if request.method == "POST":
            form = EmployeeForm(request.POST)
            eid = request.POST.get('employee_id')
            p_id = request.POST.get('personal_id')
            if form.is_valid:
                # check that user type EMP ID in DB
                if Employee.objects.filter(employee_id=eid).exists():
                    messages.info(request, 'This Employee Id Already Used!')
                else:
                    try:
                        body = {
                            "UserName": "admin_ss",
                            "Password": "ss123456*"
                        }
                        getTokenURL = 'https://p701apsi01-la02skc.azurewebsites.net/skcapi/token'
                        x = requests.post(getTokenURL, json=body).json()
                        myToken = x["accessToken"]
                        getEmpURL = f"https://p701apsi01-la01skc.azurewebsites.net/skcapi/empid/{eid}"
                        auth = {"Authorization": "Bearer %s" %myToken}
                        y = requests.get(getEmpURL, headers=auth).json()
                        nameEN = y[0]["nameEN"]
                        per_id = int(y[0]["personal_Id"])

                        if (int(per_id) == int(p_id)):
                            l.save()
                            pc = Employee(
                                line = l,
                                employee_id = eid,
                            )
                            pc.save()
                            return render(request, 'greet.html', {'nameEN': nameEN,})
                        else:
                            messages.info(request, 'Your Personal ID miss match')
                    except KeyError as e:
                        messages.info(request, 'No Employee ID in database!')
        else:
            form = EmployeeForm()
        return render(request, 'index.html')

        # if (Employee.objects.filter(employee_id=request.POST.get('employee_id')).exists()):
        #     messages.info(request, 'Already mapping')
        #     return redirect('index')
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

        #             # return redirect('greet')
        #     else:
        #         form = EmployeeForm()

        #     return render(request, 'index.html', {'form': form})

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
            return render(request, 'greet.html', {'form': form, 'nameEN': nameEN,})
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
