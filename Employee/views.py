from datetime import date

from django.shortcuts import redirect
from .forms import EmployeeResidencyForm, EmployeeForm
from .models import EmployeeResidency
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Employee
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from .utils import get_employee_by_id


# عرض جميع الموظفين
class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()  # تمرير تاريخ اليوم إلى القالب
        for employee in context['employees']:
            latest_residency = employee.residencies.order_by('-expiry_date').first()
            employee.latest_residency = latest_residency
        return context


# عرض تفاصيل الموظف
class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employee'


# إنشاء موظف جديد

class EmployeeCreateView(FormView):
    template_name = 'employee_form.html'
    form_class = EmployeeForm

    def get_context_data(self, **kwargs):
        """Get context for the form, including residency form and session data."""
        context = super().get_context_data(**kwargs)
        employee_created = self.request.session.get('employee_created', False)  # Check if employee created
        employee_id = self.request.session.get('employee_id', None)  # Retrieve employee ID if available
        employee_name = self.request.session.get('employee_name', None)
        residency_form = EmployeeResidencyForm()
        if employee_id:  # Check if employee ID exists in the session
            employee = get_employee_by_id(employee_id)
            if employee:
                employee_name = employee.name  # Retrieve the employee's name from the database
        # If an employee was created, display the residency form
        if employee_created:
            context['residency_form'] = residency_form
            context['employee_id'] = employee_id  # Include the employee ID in the context
            context['employee_created'] = True
            context['employee_name'] = employee_name
        else:
            context['residency_form'] = None  # Don't show the residency form if no employee is created yet

        return context

    def form_valid(self, form):
        """عند نجاح إنشاء الموظف، نخزن البيانات في الجلسة"""
        employee = form.save()  # حفظ الموظف
        messages.success(self.request, "✔️ تم إنشاء الموظف بنجاح! الآن قم بإضافة الإقامة.")

        # حفظ بيانات الموظف في الجلسة
        self.request.session['employee_created'] = True
        self.request.session['employee_id'] = employee.id  # تخزين ID الموظف

        return redirect('Employee:employee_create')  # إعادة تحميل الصفحة لإظهار فورم الإقامة

    def form_invalid(self, form):
        """إذا كان هناك خطأ، نعيد عرض الفورم مع الأخطاء"""
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
    """Create a new residency"""
    model = EmployeeResidency
    form_class = EmployeeResidencyForm
    template_name = "residency_form.html"
    success_url = reverse_lazy("employee_residency_list")


# تعديل بيانات الإقامة
class EmployeeResidencyUpdateView(UpdateView):
    model = EmployeeResidency
    template_name = 'residency_form.html'
    fields = ['issue_date', 'expiry_date', 'residency_file']
    success_url = reverse_lazy('employee_residency_list')


# حذف إقامة الموظف
class EmployeeResidencyDeleteView(DeleteView):
    model = EmployeeResidency
    template_name = 'employee_residency_confirm_delete.html'
    success_url = reverse_lazy('employee_residency_list')




def submit_residency(request):
    """معالجة إرسال فورم الإقامة"""
    if request.method == "POST":
        employee_id = request.session.get('employee_id', None)  # الحصول على الموظف من الجلسة

        if not employee_id:
            messages.error(request, "⚠️ لا يمكن إضافة الإقامة بدون موظف.")
            return redirect('employee_create')

        form = EmployeeResidencyForm(request.POST)
        print(form,'jjjjjjjjjjjjjjjjjjjjj')
        if form.is_valid():
            residency = form.save(commit=False)
            residency.employee = Employee.objects.get(id=employee_id)  # ربط الإقامة بالموظف
            residency.save()

            messages.success(request, "✔️ تم إنشاء الإقامة بنجاح!")

            # مسح بيانات الموظف من الجلسة لبدء عملية جديدة
            request.session['employee_created'] = False
            request.session.pop('employee_id', None)

            return redirect('Employee:employee_create')  # العودة إلى فورم الموظف

    return render(request, 'employee_form.html', {'residency_form': form})