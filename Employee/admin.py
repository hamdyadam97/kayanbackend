from django.contrib import admin
from Employee.models import Employee, EmployeeResidency

# Register your models here.


admin.site.register(Employee)
admin.site.register(EmployeeResidency)