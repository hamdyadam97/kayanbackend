from django.urls import path
from .views import EmployeeListCreateAPIView, EmployeeDetailAPIView, ResidenceCreateAPIView, \
    ResidenceRetrieveUpdateDestroyAPIView,ResidenceListAPIView

app_name = 'Employee'


urlpatterns = [
    path('', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('<slug:slug>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
    path('list/residences/', ResidenceListAPIView.as_view(), name='residence-list'),
    path('create/residences/', ResidenceCreateAPIView.as_view(), name='residence-create'),
    path('residences/<slug:slug>/', ResidenceRetrieveUpdateDestroyAPIView.as_view(), name='residence-detail'),
]

