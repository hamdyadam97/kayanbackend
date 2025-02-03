from django.urls import path
from .views import (
    EmployeeListView, EmployeeDetailView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView,
    EmployeeResidencyListView, EmployeeResidencyDetailView, EmployeeResidencyCreateView, EmployeeResidencyUpdateView, EmployeeResidencyDeleteView
)

app_name = 'Employee'

urlpatterns = [
    # Employee URLs
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/new/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),

    # Employee Residency URLs
    path('residencies/', EmployeeResidencyListView.as_view(), name='employee_residency_list'),
    path('residencies/<int:pk>/', EmployeeResidencyDetailView.as_view(), name='employee_residency_detail'),
    path('residencies/new/', EmployeeResidencyCreateView.as_view(), name='employee_residency_create'),
    path('residencies/<int:pk>/edit/', EmployeeResidencyUpdateView.as_view(), name='employee_residency_edit'),
    path('residencies/<int:pk>/delete/', EmployeeResidencyDeleteView.as_view(), name='employee_residency_delete'),
]
