from django.contrib import admin
from Employee.models import Employee

# Register your models here.


from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_deleted', 'deleted_at']  # display additional info
    list_filter = ['is_deleted']  # add filter to separate soft-deleted vs active

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Use the all_objects manager so that all records are returned.
        return qs.model.all_objects.all()

admin.site.register(Employee, EmployeeAdmin)

