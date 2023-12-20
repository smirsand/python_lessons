from django.urls import path
from education.apps import EducationConfig
from education.views import ChapterListView, MaterialListView, MaterialDetailView, TestDetailView

app_name = EducationConfig.name

urlpatterns = [
    path('', ChapterListView.as_view(), name='list_chapter'),
    path('list/<int:pk>/', MaterialListView.as_view(), name='list_materials'),
    path('material/<int:pk>/', MaterialDetailView.as_view(), name='material'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
]
