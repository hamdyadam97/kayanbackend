from .models import EmployeeResidency
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Employee
from django.urls import reverse_lazy

# عرض جميع الموظفين
class EmployeeListView(ListView):
    model = Employee
    template_name = 'pages/employee_list.html'
    context_object_name = 'employees'

# عرض تفاصيل الموظف
class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employee'

# إنشاء موظف جديد
class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'employee_form.html'
    fields = ['name', 'email', 'phone', 'start_date', 'vacation_balance']
    success_url = reverse_lazy('employee_list')

# تعديل بيانات الموظف
class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employee_form.html'
    fields = ['name', 'email', 'phone', 'start_date', 'vacation_balance']
    success_url = reverse_lazy('employee_list')

# حذف موظف
class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')


# عرض جميع إقامات الموظفين
class EmployeeResidencyListView(ListView):
    model = EmployeeResidency
    template_name = 'employee_residency_list.html'
    context_object_name = 'residencies'

# عرض تفاصيل إقامة الموظف
class EmployeeResidencyDetailView(DetailView):
    model = EmployeeResidency
    template_name = 'employee_residency_detail.html'
    context_object_name = 'residency'

# إنشاء إقامة جديدة
class EmployeeResidencyCreateView(CreateView):
    model = EmployeeResidency
    template_name = 'employee_residency_form.html'
    fields = ['employee', 'issue_date', 'expiry_date', 'residency_file']
    success_url = reverse_lazy('employee_residency_list')


# تعديل بيانات الإقامة
class EmployeeResidencyUpdateView(UpdateView):
    model = EmployeeResidency
    template_name = 'employee_residency_form.html'
    fields = ['issue_date', 'expiry_date', 'residency_file']
    success_url = reverse_lazy('employee_residency_list')


# حذف إقامة الموظف
class EmployeeResidencyDeleteView(DeleteView):
    model = EmployeeResidency
    template_name = 'employee_residency_confirm_delete.html'
    success_url = reverse_lazy('employee_residency_list')
