from django.contrib import admin
from .models import (
    Client, DebitTracking, CreditTracking, Vehicle, Sales, DieselTracking, Employee, EmployeeAttendance
)
from datetime import datetime, timedelta

# Custom filter for EmployeeAttendance
class EmployeeAttendanceFilter(admin.SimpleListFilter):
    title = 'Attendance Date'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This Week'),
            ('this_month', 'This Month'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(date=datetime.today().date())
        elif self.value() == 'this_week':
            today = datetime.today().date()
            start_week = today - timedelta(today.weekday())
            end_week = start_week + timedelta(7)
            return queryset.filter(date__range=[start_week, end_week])
        elif self.value() == 'this_month':
            today = datetime.today().date()
            return queryset.filter(date__month=today.month)
        return queryset

# Client Admin
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'address', 'created_at', 'updated_at')
    search_fields = ('name', 'contact_number', 'address')
    list_filter = ('created_at',)

# DebitTracking Admin
class DebitTrackingAdmin(admin.ModelAdmin):
    list_display = ('amount', 'payment_mode', 'type', 'description', 'date')
    search_fields = ('description', 'payment_mode', 'type')
    list_filter = ('payment_mode', 'date')

# CreditTracking Admin
class CreditTrackingAdmin(admin.ModelAdmin):
    list_display = ('amount', 'payment_mode', 'source', 'client', 'date')
    search_fields = ('source', 'description', 'client__name')
    list_filter = ('payment_mode', 'date', 'client')

# Vehicle Admin
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'registration_number', 'date_of_purchase', 'weight_capacity')
    search_fields = ('manufacturer', 'model', 'registration_number')
    list_filter = ('manufacturer', 'date_of_purchase')

# Sales Admin
class SalesAdmin(admin.ModelAdmin):
    list_display = ('client', 'vehicle', 'driver', 'weight_after_load', 'total_cost')
    search_fields = ('client__name', 'vehicle__registration_number', 'driver')
    list_filter = ('client', 'vehicle', 'created_at')

# DieselTracking Admin
class DieselTrackingAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'quantity', 'total_cost', 'purpose', 'vehicle')
    search_fields = ('supplier', 'purpose', 'vehicle__registration_number')
    list_filter = ('supplier', 'vehicle')

# Employee Admin
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'mobile_number', 'address')
    search_fields = ('name', 'designation', 'mobile_number')
    list_filter = ('designation',)

# EmployeeAttendance Admin
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'in_time', 'out_time')
    search_fields = ('employee__name', 'date')
    list_filter = (EmployeeAttendanceFilter, 'employee')

# Register models
admin.site.register(Client, ClientAdmin)
admin.site.register(DebitTracking, DebitTrackingAdmin)
admin.site.register(CreditTracking, CreditTrackingAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(DieselTracking, DieselTrackingAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeAttendance, EmployeeAttendanceAdmin)
