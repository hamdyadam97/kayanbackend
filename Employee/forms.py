from django import forms
from .models import Employee, EmployeeResidency


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'start_date', 'vacation_balance']


class EmployeeResidencyForm(forms.ModelForm):
    class Meta:
        model = EmployeeResidency
        fields = ['employee', 'issue_date', 'expiry_date', 'residency_file']
