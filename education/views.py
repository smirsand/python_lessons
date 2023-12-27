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
        test = get_object_or_404(Test, pk=kwargs['pk'])
        answer = int(request.POST.get('answer', ''))
        user = request.user

        test = get_object_or_404(Test, pk=kwargs['pk'])

        # Если ответ правильный, помечаем is_correct как True
        is_correct = (answer == test.correct_answer)

        # Проверяем, проходил ли пользователь уже этот тест
        if TestResult.objects.filter(test=test, user=user).exists():
            # Если пользователь уже проходил тест, перенаправляем на список глав
            return HttpResponseRedirect(reverse('education:list_chapter'))

        if answer:
            # Обработка правильного ответа
            test.testresult_set.create(user=user, choice=answer, is_correct=is_correct)
            material = test.material
            all_tests = Test.objects.filter(material=material).order_by('id')

            # Проверяем, все ли тесты пройдены пользователем
            if all_tests.exists():
                # Проверяем, есть ли предыдущие тесты для данного материала
                previous_tests = all_tests.filter(id__lt=test.id)
                if previous_tests.exists():
                    # Проверяем, прошел ли пользователь все предыдущие тесты
                    if not TestResult.objects.filter(test__in=previous_tests, user=user).exists():
                        # Если предыдущие тесты не пройдены, перенаправляем на последний непройденный тест
                        return HttpResponseRedirect(reverse('education:test_detail', kwargs={'pk': previous_tests.last().pk}))

                # Проверяем, есть ли еще тесты для данного материала
                remaining_tests = all_tests.filter(id__gt=test.id)
                if remaining_tests.exists():
                    # Если есть еще тесты, перенаправляем на первый непройденный тест
                    return HttpResponseRedirect(reverse('education:test_detail', kwargs={'pk': remaining_tests.first().pk}))

            # Если все тесты пройдены, перенаправляем на список глав
            return HttpResponseRedirect(reverse('education:list_chapter'))


class TestResultListView(LoginRequiredMixin, ListView):
    model = TestResult
    serializer_class = TestResultSerializer
    queryset = TestResult.objects.all()
    template_name = 'education/test_result_list.html'
    extra_context = {'title': 'Результаты теста'}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
