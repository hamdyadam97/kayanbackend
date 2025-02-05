from django.shortcuts import render

from .forms import EmployeeResidencyForm, EmployeeForm
from .models import EmployeeResidency
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Employee
from django.urls import reverse_lazy, reverse
from django.contrib import messages
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
class EmployeeCreateView(FormView):
    template_name = 'employee_form.html'  # New template for both forms
    form_class = EmployeeForm

    def get_context_data(self, **kwargs):
        """Pass both forms to the template"""
        context = super().get_context_data(**kwargs)
        context['residency_form'] = EmployeeResidencyForm()  # Residency form
        return context

    def form_valid(self, form):
        """Handle Employee creation and show Residency form"""
        employee = form.save()  # Save Employee
        messages.success(self.request, "✔️ تم إنشاء الموظف بنجاح! الآن قم بإضافة الإقامة.")

        # Pass residency form with employee pre-filled
        return render(self.request, self.template_name, {
            'residency_form': EmployeeResidencyForm(initial={'employee': employee}),
            'employee_created': True  # To hide Employee form
        })

    def form_invalid(self, form):
        """If Employee form is invalid, show errors and keep the form visible"""
        messages.error(self.request, "⚠️ يوجد خطأ في البيانات، يرجى التحقق من المدخلات.")
        return self.render_to_response(self.get_context_data(form=form))

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
