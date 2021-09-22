from django.urls import path
from .views import (
    test_tensowflow
)

app_name = 'tensorflow'

urlpatterns = [
    path('test/', test_tensorflow, name='test_tensorflow'),
]