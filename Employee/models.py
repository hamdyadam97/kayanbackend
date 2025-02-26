from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from Employee.utils import generate_unique_slug



# Choices for permit duration
DURATION_CHOICES = [
    ('3M', 'ثلاثة أشهر'),
    ('6M', 'ستة أشهر'),
    ('1Y', 'سنة كاملة'),
]

def calculate_end_date(start_date, duration):
    """Calculate the end_date based on start_date and duration."""
    if duration == '3M':
        # Add 3 months
        month = start_date.month + 3
        year = start_date.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        day = min(start_date.day, calendar.monthrange(year, month)[1])
        return start_date.replace(year=year, month=month, day=day)
    elif duration == '6M':
        month = start_date.month + 6
        year = start_date.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        day = min(start_date.day, calendar.monthrange(year, month)[1])
        return start_date.replace(year=year, month=month, day=day)
    elif duration == '1Y':
        try:
            return start_date.replace(year=start_date.year + 1)
        except ValueError:
            # For example, if start_date is February 29 in a leap year
            return start_date + (date(start_date.year + 1, 3, 1) - date(start_date.year, 3, 1))
    else:
        return start_date

def employee_image_upload(instance, filename):
    """رفع صورة الموظف إلى مسار معين داخل مجلد media"""
    return f'employee_photos/{instance.id}/{filename}'


def passport_image_upload(instance, filename):
    """رفع صورة جواز السفر"""
    return f'employee_passports/{instance.id}/{filename}'


def national_id_image_upload(instance, filename):
    """رفع صورة الهوية الوطنية"""
    return f'employee_national_ids/{instance.id}/{filename}'

def get_today_date():
    return timezone.now().date()


# Custom QuerySet to provide additional filtering if needed
class FilterAlive(models.QuerySet):
    def delete(self):
        # Instead of deleting, mark as deleted
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        # Permanently delete records
        return super().delete()

    def alive(self):
        # Return non-deleted records
        return self.filter(is_deleted=False)

    def dead(self):
        # Return soft-deleted records
        return self.filter(is_deleted=True)


# Custom Manager using the alive filter
class FilterManager(models.Manager):
    def get_queryset(self):
        return FilterAlive(self.model, using=self._db).filter(is_deleted=False)

class Employee(models.Model):
    """موديل الموظف يحتوي على جميع بيانات الموظف الأساسية والإضافية."""

    GENDER_CHOICES = [
        ('M', 'ذكر'),
        ('F', 'أنثى'),
        ('O', 'آخر')
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'أعزب'),
        ('married', 'متزوج'),
        ('divorced', 'مطلق'),
        ('widowed', 'أرمل')
    ]

    name = models.CharField(max_length=255, verbose_name="اسم الموظف")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Slug الموظف")  # رابط URL فريد
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")
    national_id = models.CharField(max_length=20, unique=True, verbose_name="رقم الهوية / جواز السفر")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="الجنس")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    hire_date = models.DateField(default=get_today_date, verbose_name="تاريخ التوظيف")
    job_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="المسمى الوظيفي")
    department = models.CharField(max_length=255, blank=True, null=True, verbose_name="القسم")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الراتب الشهري")
    leave_balance = models.IntegerField(default=30, verbose_name="رصيد الإجازات")
    is_active = models.BooleanField(default=True, verbose_name="هل الموظف نشط؟")

    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True, null=True,
                                      verbose_name="الحالة الاجتماعية")
    address = models.TextField(blank=True, null=True, verbose_name="عنوان السكن")
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True,
                                              verbose_name="اسم جهة الاتصال للطوارئ")
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الطوارئ")
    nationality = models.CharField(max_length=100, blank=True, null=True, verbose_name="الجنسية")
    work_permit_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="رقم تصريح العمل")
    bank_account_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="رقم الحساب البنكي")

    # حقول الصور
    profile_picture = models.ImageField(upload_to=employee_image_upload, blank=True, null=True,
                                        verbose_name="الصورة الشخصية")
    passport_image = models.ImageField(upload_to=passport_image_upload, blank=True, null=True,
                                       verbose_name="صورة جواز السفر")
    national_id_image = models.ImageField(upload_to=national_id_image_upload, blank=True, null=True,
                                          verbose_name="صورة الهوية الوطنية")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Managers
    objects = FilterManager()  # Default manager returns only non-deleted employees
    all_objects = models.Manager()  # Use this to access all records, including soft-deleted ones

    def delete(self, using=None, keep_parents=False):
        """Override delete to perform a soft delete."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete the record."""
        super().delete(using=using, keep_parents=keep_parents)


    def save(self, *args, **kwargs):
        # Generate unique slug if not provided.
        if not self.slug and self.name:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.job_title}"

    class Meta:
        verbose_name = "الموظف"
        verbose_name_plural = "الموظفون"
        ordering = ['name']





class Residence(models.Model):
    """
    نموذج إقامة الموظف.
    كل موظف يمكن أن يكون له إقامة واحدة نشطة في وقت واحد.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='residences', verbose_name="الموظف")
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES, verbose_name="مدة الإقامة")
    start_date = models.DateField(default=timezone.now, verbose_name="تاريخ بدء الإقامة")
    end_date = models.DateField(blank=True, null=True, verbose_name="تاريخ انتهاء الإقامة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    def clean(self):
        """
        Ensure that there is no active residence for this employee.
        An active residence is one whose end_date is greater than or equal to today.
        """
        active_residences = Residence.objects.filter(employee=self.employee, end_date__gte=timezone.now().date())
        if self.pk:
            active_residences = active_residences.exclude(pk=self.pk)
        if active_residences.exists():
            raise ValidationError("يوجد إقامة سارية للموظف. يجب انتهاء الإقامة الحالية قبل إنشاء إقامة جديدة.")

    def save(self, *args, **kwargs):
        # Automatically calculate the end_date if not provided
        if not self.end_date:
            self.end_date = calculate_end_date(self.start_date, self.duration)
        self.full_clean()  # This will call clean() and raise errors if any.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"إقامة {self.employee.name} من {self.start_date} إلى {self.end_date}"