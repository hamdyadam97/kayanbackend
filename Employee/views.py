from rest_framework import generics, status
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    """
    API to list all employees and create a new employee.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        """Override GET response format"""
        employees = self.get_queryset()
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Override POST response format"""
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import get_object_or_404

class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API to retrieve, update, or delete a specific employee.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'slug'  # Tells DRF to use the slug field for lookups

    # If you wish to override methods, for example, retrieve:
    def retrieve(self, request, *args, **kwargs):
        employee = get_object_or_404(Employee, slug=kwargs["slug"])
        serializer = self.get_serializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        employee = get_object_or_404(Employee, slug=kwargs["slug"])
        serializer = self.get_serializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        employee = get_object_or_404(Employee, slug=kwargs["slug"])
        employee.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
