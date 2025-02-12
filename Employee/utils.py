from Employee.models import Employee


def get_employee_by_id(employee_id):
    employees = Employee.objects.filter(id=employee_id)  # Use filter to get a queryset
    if employees.exists():  # Check if the queryset contains any employees
        return employees.first()  # Return the first (and only) employee
    return None

