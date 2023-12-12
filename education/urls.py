from django.urls import path

from education.views import index

urlpatterns = [
    path('', index)
]