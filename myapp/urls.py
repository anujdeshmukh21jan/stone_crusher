from django.urls import path
from . import views

urlpatterns = [
    path("update_constants/", views.constants, name="update_constants"),
    path('', views.sales, name='sales'),
    path('vehicles/', views.vehicles, name='vehicles'), 
    path('payments/', views.payments, name='payments'), 
    path('employees/', views.employees, name='employees'),
    path('diesel/', views.diesel, name='diesel'), 
    path('add-employee', views.add_employee, name='add_employee'),
    path('add-client', views.add_client, name='add_client'),
    path('reports/vehicles_report/', views.vehicles_report, name='vehicles_report'),
    path('reports/sales_report/', views.sales_report, name='sales_report'),
    path('reports/credit_report/', views.credit_report, name='credit_report'),
    path('reports/debit_report/', views.debit_report, name='debit_report'),
    path('reports/clients_report/', views.clients_report, name='clients_report'),
    path('reports/attendence_report/', views.attendence_report, name='attendence_report'),
    path('reports/employees_report/', views.employees_report, name='employees_report'),
    path('get_constants_data/', views.get_constants_data, name='get_constants_data'),
]
