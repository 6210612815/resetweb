from telnetlib import KERMIT
from django.shortcuts import render, redirect
from django.contrib import messages
from database.models import Employee, EmployeeForm
import requests

def index(request):
    """
    USER_ID = get userID from LIFF

    IF USER_ID NOT IN DB:
        a = LineID(user_id='USER_ID')
        a.save()

        SHOW FORM & SAVED
        

         & APPEND IN DB
    ELSE:
        RETURN GREETING PAGE
    """

    try:
        user = 'Uaa37289a5faf8eb0f26b689216a67f58'
        employee = Employee.objects.get(user_id=user)
        

        body = {
            "UserName": "admin_ss",
            "Password": "ss123456*"
        }
        getTokenURL = 'https://p701apsi01-la02skc.azurewebsites.net/skcapi/token'
        x = requests.post(getTokenURL, json=body).json()
        myToken = x["accessToken"]
        eid = employee.employee_id
        getEmpURL = f"https://p701apsi01-la01skc.azurewebsites.net/skcapi/empid/{eid}"
        auth = {"Authorization": "Bearer %s" %myToken}
        y = requests.get(getEmpURL, headers=auth).json()
        nameEN = y[0]["nameEN"]
        data = {
                'nameEN': nameEN,
            }
        return render(request, 'greet.html', data)

    except Employee.DoesNotExist:
        if request.method == "POST":
            form = EmployeeForm(request.POST)
            if form.is_valid:
                form.save()
        else:
            form = EmployeeForm()
        return render(request, 'index.html', {'form': form})


    

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
            return render(request, 'greet.html', data)
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
