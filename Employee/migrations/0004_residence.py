# Generated by Django 5.1.6 on 2025-02-27 10:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0003_employee_deleted_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug الإقامة')),
                ('duration', models.CharField(choices=[('3M', 'ثلاثة أشهر'), ('6M', 'ستة أشهر'), ('1Y', 'سنة كاملة')], max_length=3, verbose_name='مدة الإقامة')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاريخ بدء الإقامة')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='تاريخ انتهاء الإقامة')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='محذوف؟')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='تاريخ الحذف')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='residences', to='Employee.employee', verbose_name='الموظف')),
            ],
        ),
    ]
