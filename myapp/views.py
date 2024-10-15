from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .utils import modify_env_file
from django.db.models import Max
from .models import *
#import reverce, redirect
from django.urls import reverse

# Create your views here.
def base(request):
    return render(request, "base.html")


from django.http import JsonResponse

def sales(request):
    if request.method == "GET":
        max_id = Sales.objects.aggregate(Max('id'))['id__max']
        client_names = Client.objects.all()
        client_names = [client.name for client in client_names]
        vehicle_numbers = Vehicle.objects.all()
        vehicle_numbers_with_weight = {
            i.registration_number: str(i.weight_capacity) for i in vehicle_numbers
        }
        context = {
            "client_names": json.dumps(client_names),
            "vehicle_numbers": json.dumps(vehicle_numbers_with_weight),
            "bill_no": max_id+1
        }
        return render(request, "sales.html", context=context)

    elif request.method == "POST":
        # Extract form data
        context = {}
        try:
            name = request.POST.get("name")
            vehicle_number = request.POST.get("vehicle_number")
            driver_name = request.POST.get("driver_name")
            weight_after_load = request.POST.get("weight_after_load")

            # Optional: Collect size and prices
            size_data = {
                "6mm": request.POST.get("size_6mm"),
                "12mm": request.POST.get("size_12mm"),
                "20mm": request.POST.get("size_20mm"),
                "40mm": request.POST.get("size_40mm"),
                "60mm": request.POST.get("size_60mm"),
                "GSB": request.POST.get("size_GSB"),
                "KK": request.POST.get("size_KK"),
            }
            
            total_cost = 0
            for i in size_data:
                if size_data[i] is not None:
                    key = f'value_size_{i}'
                    total_cost+=int(request.POST.get(key))
            print(total_cost)
            
            if name and vehicle_number and driver_name and weight_after_load:
                sale = Sales(
                    client=Client.objects.get(name=name),
                    vehicle=Vehicle.objects.get(registration_number=vehicle_number),
                    driver=driver_name,
                    weight_after_load=weight_after_load,
                    size=size_data,
                    total_cost=total_cost
                )
                sale.save()
                context = {"success": "true"}
            context = {"success": "false"}
        except:
            context = {"success": "false"}
        finally:
            return redirect(reverse('sales'))


def vehicles(request):
    if request.method == "GET":
        return render(request, "vehicles.html")
    elif request.method == "POST":
        context = {}
        try:
            print(request.POST)
            manufacturer = request.POST.get("manufacturer")
            model = request.POST.get("model")
            registration_number = request.POST.get("registration_number")
            date_of_purchase = request.POST.get("date_of_purchase")
            weight = request.POST.get("weight")
            if manufacturer and model and registration_number and weight:
                vehicle = Vehicle(
                    manufacturer=manufacturer,
                    model=model,
                    registration_number=registration_number,
                    date_of_purchase=date_of_purchase,
                    weight_capacity=weight,
                )
                vehicle.save()
                context = {"success": "true"}
            else:
                context = {"success": "false"}
        except Exception as e:
            context = {"success": "false"}
        finally:
            return render(request, "vehicles.html", context)


def payments(request):
    return render(request, "payments.html")


def employees(request):
    return render(request, "employees.html")


def reports(request):
    return render(request, "reports.html")


def constants(request):
    if request.method == "GET":
        return render(request, "constants.html")
    elif request.method == "POST":
        print(request.POST)
        modify_env_file(request.POST, ".env")
        return JsonResponse({"success": "true"})


def add_client(request):
    if request.method == "POST":
        client_name = request.POST.get("client-name")
        contact_number = request.POST.get("contact-number")
        address = request.POST.get("address")

        if client_name and contact_number and address:
            client = Client(name=client_name, contact_number=contact_number, address=address)
            client.save()
            print(client)
            return JsonResponse(
                {"success": True, "message": "Client added successfully"}
            )
        else:
            return JsonResponse({"success": False, "error": "All fields are required"})

    return JsonResponse({"success": False, "error": "Invalid request"})


def sales_report(request):
    return render(request, "reports/sales_report.html")

def vehicles_report(request):
    return render(request, "reports/vehicles_report.html")

def payments_report(request):
    return render(request, "reports/payments_report.html")

def employees_report(request):
    return render(request, "reports/employees_report.html")

def clients_report(request):
    return render(request, "reports/clients_report.html")

def attendence_report(request):
    return render(request, "reports/attendence.html")