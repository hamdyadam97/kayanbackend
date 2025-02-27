from rest_framework import serializers
from .models import Employee, Residence
from django.core.exceptions import ValidationError as DjangoValidationError

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer to convert Employee Model to JSON"""

    class Meta:
        model = Employee
        fields = '__all__'  # Include all fields



class ResidenceSerializer(serializers.ModelSerializer):
    # This will accept an employee slug on input and output the slug on serialization
    employee = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        slug_field='slug',
        write_only=True
    )

    def validate(self, data):
        # Create an instance with the data to run model-level validations (i.e. clean())
        instance = Residence(**data)
        try:
            instance.full_clean()  # This calls clean() on the model
        except DjangoValidationError as exc:
            # Optionally reformat the error messages.
            # For example, remove the '__all__' key and use 'non_field_errors'
            errors = exc.message_dict
            if '__all__' in errors:
                errors['non_field_errors'] = errors.pop('__all__')
            raise serializers.ValidationError(errors)
        return data
    employee_detail = EmployeeSerializer(source='employee', read_only=True)
    class Meta:
        model = Residence
        fields = '__all__'

