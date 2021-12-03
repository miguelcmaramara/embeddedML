from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('submitgesture/', views.snippet_list),
    path('submitgesture/<str:pk>', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)