from django.shortcuts import render
# HttpResponse
from django.http import HttpResponse

from datetime import datetime

import random

# Create your views here.
def sayhello(request):
    return HttpResponse('Hello, Django!')

def hello2(request, username):
    return HttpResponse(f'Hello Django, {username}!')

def hello3(request, username):
    # 抓現在時間
    now = datetime.now()
    #                                     {"now": "value", "username": "value"}
    return render(request, 'app001/hello3.html', locals())

def hello4(request, username):
    # 抓現在時間
    now = datetime.now()
    #                                     {"now": "value", "username": "value"}
    return render(request, 'app001/hello4.html', locals())

def dice(request):
    no1 = random.randint(1, 6)
    no2 = random.randint(1, 6)
    no3 = random.randint(1, 6)
    return render(request, 'app001/dice.html', locals())

def employee(request):
    employee1 = {"name":"Amy","phone":"049-1234567","age":20}
    employee2 = {"name":"Jack","phone":"02-4455666","age":25}
    employee3 = {"name":"Nacy","phone":"04-9876543","age":17}
    employees = [employee1, employee2, employee3]
    return render(request, "app001/employee.html", locals())