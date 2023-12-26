from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from rest_framework.generics import get_object_or_404

from education.forms import TestResultForm, TestForm
from education.models import Chapter, Material, Test, TestResult
from education.serliazers import ChapterSerializer, MaterialSerializer, TestSerializer, TestResultSerializer


class ChapterListView(LoginRequiredMixin, ListView):
    model = Chapter
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    template_name = 'education/home.html'
    extra_context = {'title': 'Главная'}


class ChapterDetailView(LoginRequiredMixin, DetailView):
    model = Chapter
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    template_name = 'education/materials_list.html'
    extra_context = {'title': 'Материалы раздела'}


class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    template_name = 'education/materials_list.html'
    extra_context = {'title': 'Список материалов раздела'}

    def get_queryset(self):
        chapter_id = self.kwargs['pk']
        return Material.objects.filter(chapter_id=chapter_id)


class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    template_name = 'education/material_detail.html'
    extra_context = {'title': 'Материал'}


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    serializer_class = TestSerializer
    template_name = 'education/test_list.html'
    extra_context = {'title': 'Список тестов'}

    def get_queryset(self):
        material_id = self.kwargs['material_id']
        material = get_object_or_404(Material, id=material_id)
        return Test.objects.filter(material=material)


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    form_class = TestForm
    template_name = 'education/test_detail.html'
    extra_context = {'title': 'Тест'}

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = self.object.material.test_set.values_list('id', flat=True)
        return context

    def post(self, request, *args, **kwargs):
        test = self.get_object()
        answer = request.POST.get('answer', '')
        user = request.user

        if answer:
            # Обработка правильного ответа
            test.testresult_set.create(user=user, choice=answer)
            material = test.material
            next_tests = Test.objects.filter(material=material, id__gt=test.id).order_by('id')

            # Проверяем, остались ли еще тесты для данного материала
            if next_tests.exists():
                # Находим следующий тест
                next_test = next_tests.first()

                # Перенаправляем на следующий тест
                return HttpResponseRedirect(reverse('education:test_detail', kwargs={'pk': next_test.pk}))
            else:
                # Перенаправляем на список глав, если больше нет тестов
                return HttpResponseRedirect(reverse('education:list_chapter'))
        else:
            # Перенаправляем на текущий тест, если пользователь не отправил ответ
            return HttpResponseRedirect(reverse('education:test_detail', kwargs={'pk': test.pk}))


class TestResultListView(LoginRequiredMixin, ListView):
    model = TestResult
    serializer_class = TestResultSerializer
    queryset = TestResult.objects.all()
    template_name = 'education/test_result_detail.html'
    extra_context = {'title': 'Результаты теста'}
