from django.urls import path
from . import views

urlpatterns = [
    path("update_constants/", views.constants, name="update_constants"),
    path('', views.sales, name='sales'),
    path('vehicles/', views.vehicles, name='vehicles'), 
    path('payments/', views.payments, name='payments'), 
    path('employees/', views.employees, name='employees'),
    path('reports/', views.reports, name='reports'), 
]
