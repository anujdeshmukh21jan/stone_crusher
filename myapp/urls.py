from django.urls import path
from . import views

urlpatterns = [
    # path('', views.base, name='base'), 
    path('', views.sales, name='sales'),
    path('vehicles/', views.vehicles, name='vehicles'), 
    path('payments/', views.payments, name='payments'), 
    path('employees/', views.employees, name='employees'), 
]
