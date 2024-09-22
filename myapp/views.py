from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import modify_env_file


# Create your views here.
def base(request):
    return render(request,"base.html")

def sales(request):
    return render(request, 'sales.html')

def vehicles(request):
    return render(request, 'vehicles.html')

def payments(request):
    return render(request, 'payments.html')

def employees(request):
    return render(request, 'employees.html')

def reports(request):
    return render(request, 'reports.html')

def constants(request):
    if request.method=="GET":
        return render(request, "constants.html")
    elif request.method=="POST":
        print(request.POST)
        modify_env_file(request.POST, ".env")
        return JsonResponse({"success":"true"})