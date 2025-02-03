from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from datetime import timedelta


class Employee(models.Model):
    """ نموذج الموظف الأساسي """
    name = models.CharField(max_length=255, verbose_name='اسم الموظف')
    email = models.EmailField(unique=True, verbose_name='البريد الإلكتروني')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='رقم الهاتف')
    start_date = models.DateField(verbose_name='تاريخ بدء العمل')
    vacation_balance = models.PositiveIntegerField(default=21, verbose_name='رصيد الإجازات (بالأيام)')
    image = models.ImageField(upload_to='Employee/', verbose_name="صورة الموظف ", null=True, blank=True)

    def __str__(self):
        return self.name


class EmployeeResidency(models.Model):
    """إقامة الموظف وتجديدها سنويًا"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='residencies', verbose_name="الموظف")
    issue_date = models.DateField(verbose_name="تاريخ إصدار الإقامة")
    expiry_date = models.DateField(verbose_name="تاريخ انتهاء الإقامة")
    residency_file = models.FileField(upload_to='residencies/', verbose_name="ملف الإقامة", null=True, blank=True)

    def __str__(self):
        return f"إقامة {self.employee.name} تنتهي في {self.expiry_date}"

    def is_expiring_soon(self):
        """للتحقق مما إذا كانت الإقامة ستنتهي خلال 30 يومًا"""
        return self.expiry_date <= now().date() + timedelta(days=30)

    def renew_residency(self):
        """تجديد الإقامة للسنة التالية"""
        self.expiry_date = self.expiry_date.replace(year=self.expiry_date.year + 1)
        self.save()

    def clean(self):
        """التحقق من أنه لا يمكن رفع الإقامة إذا كانت قد تم تجديدها"""
        if self.pk is None:  # فقط إذا كانت الإقامة جديدة (لم يتم حفظها بعد)
            last_residency = EmployeeResidency.objects.filter(employee=self.employee).last()
            if last_residency and last_residency.expiry_date > now().date():
                raise ValidationError("لا يمكن رفع إقامة جديدة لأن الإقامة الحالية قد تم تجديدها للسنة الحالية.")

    class Meta:
        verbose_name = "إقامة الموظف"
        verbose_name_plural = "إقامات الموظفين"

