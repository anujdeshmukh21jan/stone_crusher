from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"home.html")

def vehicles(request):
    return render(request,"vehicles.html")

def payments(request):
    return render(request,"payments.html")

def employees(request):
    return render(request,"employees.html")