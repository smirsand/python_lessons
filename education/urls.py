from django.urls import path

from education.apps import EducationConfig
from education.views import ChapterListView, MaterialListView, MaterialDetailView, TestDetailView, TestResultListView, \
    TestListView

app_name = EducationConfig.name

urlpatterns = [
    path('', ChapterListView.as_view(), name='chapter_list'),
    path('chapters/<int:pk>/', MaterialListView.as_view(), name='material_list'),
    path('material/<int:pk>/', MaterialDetailView.as_view(), name='material_detail'),
    path('tests/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('materials/<int:material_id>/', TestListView.as_view(), name='test_list'),
    path('results/', TestResultListView.as_view(), name='test_result_list'),
]
