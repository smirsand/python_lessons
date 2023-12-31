from django.urls import path

from education.apps import EducationConfig
from education.views import ChapterListView, MaterialListView, MaterialDetailView, TestDetailView, TestResultListView, \
    TestListView

app_name = EducationConfig.name

urlpatterns = [
    path('', ChapterListView.as_view(), name='list_chapter'),
    path('list/<int:pk>/', MaterialListView.as_view(), name='list_materials'),
    path('material/<int:pk>/', MaterialDetailView.as_view(), name='material'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('test_list/<int:material_id>/', TestListView.as_view(), name='test_list'),
    path('result_list/', TestResultListView.as_view(), name='list_result'),
]
