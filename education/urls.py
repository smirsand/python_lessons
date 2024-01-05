from django.urls import path

from education.apps import EducationConfig
from education.views import ChapterListView, MaterialListView, MaterialDetailView, TestDetailView, TestResultListView, \
    TestListView, ChapterRetrieveAPIView, MaterialRetrieveAPIView, TestRetrieveAPIView, TestResultRetrieveAPIView, \
    TestResultListAPIView, TestResultCreateAPIView

app_name = EducationConfig.name

urlpatterns = [
    path('', ChapterListView.as_view(), name='list_chapter'),
    path('chapter/<int:pk>/', ChapterRetrieveAPIView.as_view(), name='chapter_retrieve'),
    path('list/<int:pk>/', MaterialListView.as_view(), name='list_materials'),
    path('material/<int:pk>/', MaterialDetailView.as_view(), name='material'),
    path('material/<int:pk>/', MaterialRetrieveAPIView.as_view(), name='material_retrieve'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('test/<int:pk>/', TestRetrieveAPIView.as_view(), name='test_retrieve'),
    path('test_list/<int:material_id>/', TestListView.as_view(), name='test_list'),
    path('result/create/', TestResultCreateAPIView.as_view(), name='result_create'),
    path('result_list/', TestResultListView.as_view(), name='list_result'),
    path('results_list/<int:pk>/', TestResultListAPIView.as_view(), name='list_results'),
    path('result/<int:pk>/', TestResultRetrieveAPIView.as_view(), name='result_retrieve'),
]
