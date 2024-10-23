from django.db import models
import json
import ast


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Client(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class DebitTracking(BaseModel):
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50)  # e.g., Cash, Bank Transfer
    type = models.CharField(max_length=100)  # e.g., Client, Employee
    quantity = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255)  # e.g., Salary, Purchase

    def __str__(self):
        return f"Debit - {self.amount} on {self.date}"


class CreditTracking(BaseModel):
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50)  # e.g., Cash, Bank Transfer
    source = models.CharField(max_length=100)  # e.g., Project, Loan (if not client)
    description = models.CharField(max_length=255, blank=True)  # Optional description of the source
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)  # Link to Client

    def __str__(self):
        return f"Credit - {self.amount} from {self.client.name if self.client else 'N/A'} on {self.date}"


class Vehicle(BaseModel):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50, unique=True)
    date_of_purchase = models.DateField()
    weight_capacity = models.DecimalField(max_digits=10, decimal_places=2)  # Maximum weight the vehicle can carry

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.registration_number})"


class Sales(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.CharField(max_length=100, null=True, blank=True)
    weight_after_load = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def get_sizes_list(self):
        data_dict = ast.literal_eval(self.size)  # Convert string to dictionary

        result = ', '.join([key for key, value in data_dict.items() if value is None])
        return result

    @property
    def weight_before_load(self):
        return self.vehicle.weight_capacity
    
    @property
    def total_load_weight(self):
        return self.weight_after_load-self.weight_before_load
    
    @property
    def total_load_weight_in_tonnes(self):
        return self.total_load_weight/1000
    
    @property
    def total_load_weight_in_brass(self):
        return self.total_load_weight/4
    
    def __str__(self):
        return f"Sale - {self.client.name} ({self.id})"


class DieselTracking(BaseModel):
    supplier = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=100, blank=True, null=True)  # e.g., Generator, Vehicle, etc.
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)  # Optional link to Vehicle

    def __str__(self):
        return f"Diesel - {self.supplier} ({self.quantity}L)"


class Employee(BaseModel):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    mobile_number = models.CharField(null=True, blank=True, max_length=15)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class EmployeeAttendance(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name}"
