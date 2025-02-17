from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer to convert Employee Model to JSON"""

    class Meta:
        model = Employee
        fields = '__all__'  # Include all fields




