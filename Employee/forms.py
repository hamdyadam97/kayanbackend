from django import forms
from .models import Employee, EmployeeResidency


from django import forms
from .models import Employee
from django.core.exceptions import ValidationError
import re


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'start_date', 'vacation_balance', 'image']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        name_regex = r"^[A-Za-z\u0600-\u06FF ]{20,}$"  # Arabic & English letters, min 20 chars
        if not re.match(name_regex, name):
            raise ValidationError("يجب أن يكون الاسم 20 حرفًا على الأقل ولا يحتوي على رموز خاصة")
        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            raise ValidationError("يرجى إدخال بريد إلكتروني صالح")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        phone_regex = r"^(?:\+9665|05)\d{8}$"  # Saudi Arabia format
        if not re.match(phone_regex, phone):
            raise ValidationError("يجب أن يكون رقم الهاتف بصيغة سعودية صحيحة (05xxxxxxxx أو +9665xxxxxxxx)")
        return phone

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            allowed_types = ["image/jpeg", "image/png", "image/gif"]
            if image.content_type not in allowed_types:
                raise ValidationError("يجب أن يكون الملف صورة بصيغة JPG أو PNG أو GIF")
        return image



class EmployeeResidencyForm(forms.ModelForm):
    class Meta:
        model = EmployeeResidency
        fields = ['employee', 'issue_date', 'expiry_date', 'residency_file']
