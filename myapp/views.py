from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .utils import modify_env_file
from django.db.models import Max
import os
from .models import *
#import reverce, redirect
from django.urls import reverse
# import Q
from django.db.models import Q



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
    if request.method == "GET":
        clients = Client.objects.all()
        context = {"clients": clients}
        return render(request, "payments.html", context=context)
    elif request.method == "POST":
        payload = request.POST
        type_of_trans = payload.get("type")
        client_name = payload.get("client_name")
        amount = payload.get("amount")
        payment_type = payload.get("payment_type")
        description = payload.get("description")
        debit_type = payload.get("debit_type")
        diesel_quantity = payload.get("diesel_quantity")
        print(type_of_trans, client_name, amount, payment_type, description, debit_type, diesel_quantity)
        if type_of_trans == "debit":
            if debit_type == "diesel":
                DebitTracking.objects.create(
                    amount=amount,
                    payment_mode=payment_type,
                    type=debit_type,
                    description=description,
                    quantity=diesel_quantity,
                )
            else:
                DebitTracking.objects.create(
                    amount=amount,
                    payment_mode=payment_type,
                    type=debit_type,
                    description=description,
                )
        elif type_of_trans == "credit":
            CreditTracking.objects.create(
                amount=amount, payment_mode=payment_type, description=description,
                source=client_name
            )
        return render(request, "payments.html")


def employees(request):
    if request.method == "GET":
        employees = Employee.objects.all()
        employees_names = [employee.name for employee in employees]
        context = {"employees": json.dumps(employees_names)}
        return render(request, "employees.html", context=context)
    elif request.method == "POST":
        print(request.POST)
        payload = request.POST
        name = payload.get("name")
        date = payload.get("date")
        in_time = payload.get("in-time")
        out_time = payload.get("out-time")
        if name and in_time and out_time:
            employee = EmployeeAttendance(
                employee=Employee.objects.get(name=name),
                date=date,
                in_time=in_time,
                out_time=out_time
            )
            employee.save()
            print(employee)
        return render(request, "employees.html")
    
def diesel(request):
    return render(request, "diesel.html")

def constants(request):
    if request.method == "POST":
        print(request.POST)
        modify_env_file(request.POST, ".env")
        return JsonResponse({"success": "true"})

def add_employee(request):
    if request.method == "POST":
        print(request.POST)
        employee_name = request.POST.get("employee-name")
        employee_designation = request.POST.get("employee-designation")
        contact_number = request.POST.get("contact-number")
        address = request.POST.get("address")
        if employee_name and employee_designation and contact_number and address:
            employee = Employee(name=employee_name, designation=employee_designation, mobile_number=contact_number, address=address)
            employee.save()
            print(employee)
            return JsonResponse(
                {"success": True, "message": "Employee added successfully"}
            )
        else:
            return JsonResponse({"success": False, "error": "All fields are required"})

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

def get_constants_data(request):
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "r") as file:
            lines = file.readlines()
    else:
        lines = []
    constants_data = {}
    for i in lines:
        key = i.split('=')[0].strip()
        value = i.split('=')[1].strip()
        constants_data[key] = value
    print(constants_data)
    return JsonResponse(constants_data)

def sales_report(request):
    sales = Sales.objects.all()
    filters = {}
    if request.GET.get("search"):
        filters["client__name__icontains"] = request.GET.get("search")
    if request.GET.get("from_date"):
        filters["created_at__gte"] = request.GET.get("from_date")
    if request.GET.get("to_date"):
        filters["created_at__lte"] = request.GET.get("to_date")
    if request.GET.get("bill_no"):
        filters["id"] = request.GET.get("bill_no")
    if request.GET.get("name"):
        filters["client__name__icontains"] = request.GET.get("name")
    if request.GET.get("driver_name"):
        filters["driver__icontains"] = request.GET.get("driver_name")
    if request.GET.get("vehicle_no"):
        filters["vehicle__registration_number__icontains"] = request.GET.get(
            "vehicle_no"
        )
    sales = sales.filter(**filters)
    print(sales)
    return render(request, "reports/sales_report.html", context={"sales": sales})

def vehicles_report(request):
    if request.method == "GET":
        vehicles = Vehicle.objects.all()
        search  = request.GET.get("search")
        if search:
            vehicles = vehicles.filter(
                Q(registration_number__icontains=search) |
                Q(manufacturer__icontains=search) |
                Q(model__icontains=search)
            )
        context = {"vehicles": vehicles}
        return render(request, "reports/vehicles_report.html", context=context)
    return render(request, "reports/vehicles_report.html")

def credit_report(request):
    if request.method == "GET":
        credits = CreditTracking.objects.all()
        search  = request.GET.get("search")
        print(request.GET)
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        if from_date:
            credits = credits.filter(created_at__gte=from_date)
        if to_date:
            credits = credits.filter(created_at__lte=to_date)
        if search:
            credits = credits.filter(
                Q(description__icontains=search) |
                Q(payment_mode__icontains=search) |
                Q(client__name__icontains=search) |
                Q(amount__icontains=search)
            )
        context = {"credits": credits}
        return render(request, "reports/credit_report.html", context=context)
    return render(request, "reports/credit_report.html")

def debit_report(request):
    if request.method == "GET":
        debits = DebitTracking.objects.all()
        search  = request.GET.get("search")
        print(request.GET)
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        if from_date:
            debits = debits.filter(created_at__gte=from_date)
        if to_date:
            debits = debits.filter(created_at__lte=to_date)
        if search:
            debits = debits.filter(
                Q(description__icontains=search) |
                Q(payment_mode__icontains=search) |
                Q(type=search) |
                Q(amount__icontains=search)
            )
        print(debits)
        context = {"debits": debits}
        return render(request, "reports/debit_report.html", context=context)
    return render(request, "reports/debit_report.html")

def employees_report(request):
    if request.method == "GET":
        employees = Employee.objects.all()
        search  = request.GET.get("search")
        if search:
            employees = employees.filter(
                Q(name__icontains=search) |
                Q(designation__icontains=search) |
                Q(mobile_number__icontains=search)
            )
        context = {"employees": employees}
        return render(request, "reports/employees_report.html", context=context)
    
    return render(request, "reports/employees_report.html")

def clients_report(request):
    if request.method == "GET":
        clients = Client.objects.all()
        search  = request.GET.get("search")
        if search:
            clients = clients.filter(
                Q(name__icontains=search) |
                Q(contact_number__icontains=search) |
                Q(address__icontains=search)
            )
        context = {"clients": clients}
        return render(request, "reports/clients_report.html", context=context)

from datetime import datetime, timedelta

def get_date_range(from_date, to_date):
    start_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(to_date, "%Y-%m-%d").date()
    delta = timedelta(days=1)
    
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += delta
    return date_list


def attendence_report(request):
    if request.method == "GET":
        employees = Employee.objects.all()
        employee_id = request.GET.get("name")
        response_data = []

        if employee_id:
            from_date = request.GET.get("from_date")
            to_date = request.GET.get("to_date")
            
            attendence = EmployeeAttendance.objects.filter(employee__id=employee_id)
            response_data = attendence
            if from_date and to_date:
                # Generate date range
                response_data =[]
                date_range = get_date_range(from_date, to_date)

                # Fetch attendance data within the range
                attendence = attendence.filter(date__range=[from_date, to_date])

                # Create a dictionary for attendance on each date
                attendance_by_date = {attendance.date: attendance for attendance in attendence}

                # Prepare JSON response
                for date in date_range:
                    attendance_record = attendance_by_date.get(date)
                    if attendance_record:
                        response_data.append({
                            "date": date.strftime("%Y-%m-%d"),
                            "in_time": attendance_record.in_time.strftime("%H:%M:%S") if attendance_record.in_time else None,
                            "out_time": attendance_record.out_time.strftime("%H:%M:%S") if attendance_record.out_time else None,
                        })
                    else:
                        response_data.append({
                            "date": date.strftime("%Y-%m-%d"),
                            "in_time": None,
                            "out_time": None,
                        })

        context = {
            "attendence": response_data,
            "employees": employees,
        }
        return render(request, "reports/attendence.html", context=context)
    
    return render(request, "reports/attendence.html")
