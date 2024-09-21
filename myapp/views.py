from django.shortcuts import render

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