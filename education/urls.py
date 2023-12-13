from django.urls import path

from education.apps import EducationConfig
from education.views import ChapterListView, ChapterDetailView, MaterialsListView

app_name = EducationConfig.name

urlpatterns = [
    path('', ChapterListView.as_view(), name='list_chapter'),
    path('list/<int:pk>/', MaterialsListView.as_view(), name='list_materials'),

    # path('', MaterialsListView.as_view(), name='list_chapter'),
]
