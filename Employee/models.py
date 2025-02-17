from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now


def employee_image_upload(instance, filename):
    """رفع صورة الموظف إلى مسار معين داخل مجلد media"""
    return f'employee_photos/{instance.id}/{filename}'


def passport_image_upload(instance, filename):
    """رفع صورة جواز السفر"""
    return f'employee_passports/{instance.id}/{filename}'


def national_id_image_upload(instance, filename):
    """رفع صورة الهوية الوطنية"""
    return f'employee_national_ids/{instance.id}/{filename}'


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
    hire_date = models.DateField(default=now, verbose_name="تاريخ التوظيف")
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

    def save(self, *args, **kwargs):
        """توليد slug تلقائيًا إذا لم يتم توفيره."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.job_title}"

    class Meta:
        verbose_name = "الموظف"
        verbose_name_plural = "الموظفون"
        ordering = ['name']


