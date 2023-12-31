from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from rest_framework.generics import get_object_or_404

from education.forms import TestForm
from education.models import Chapter, Material, Test, TestResult
from education.serliazers import ChapterSerializer, MaterialSerializer, TestSerializer, TestResultSerializer
from users.models import User


class ChapterListView(LoginRequiredMixin, ListView):
    """
    Контроллер списка разделов.
    """
    model = Chapter
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    template_name = 'education/home.html'
    extra_context = {'title': 'Главная'}


class MaterialListView(LoginRequiredMixin, ListView):
    """
    Контроллер списка материалов.
    """
    model = Material
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    template_name = 'education/materials_list.html'
    extra_context = {'title': 'Список материалов раздела'}

    def get_queryset(self):
        chapter_id = self.kwargs['pk']
        return Material.objects.filter(chapter_id=chapter_id)


class MaterialDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер материала.
    """
    model = Material
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    template_name = 'education/material_detail.html'
    extra_context = {'title': 'Материал'}


class TestListView(LoginRequiredMixin, ListView):
    """
    Контроллер списка тестов.
    """
    model = Test
    serializer_class = TestSerializer
    template_name = 'education/test_list.html'
    extra_context = {'title': 'Список тестов'}

    def get_queryset(self):
        # Получаем material_id из параметров представления.
        material_id = self.kwargs['material_id']
        # Получаем объект Material по material_id.
        material = get_object_or_404(Material, id=material_id)
        # Получаем id текущего пользователя из запроса.
        user_id = self.request.user.id
        # Получаем список тестов, которые не пройдены текущим пользователем.
        completed_test_ids = TestResult.objects.filter(user_id=user_id).values_list('test_id', flat=True)
        # Фильтруем тесты на основе тех, которые не были пройдены пользователем.
        queryset = Test.objects.filter(material=material).exclude(id__in=completed_test_ids)

        return queryset


class TestDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер теста.
    """
    model = Test
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    form_class = TestForm
    template_name = 'education/test_detail.html'
    extra_context = {'title': 'Тест'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = self.get_object()
        user = self.request.user
        context['tests'] = [{
            'test': test,
            'completed': TestResult.objects.filter(test=test, user=user).exists()
        }]
        return context

    def post(self, request, *args, **kwargs):
        test = get_object_or_404(Test, pk=kwargs['pk'])
        answer = int(request.POST.get('answer', ''))
        user_id = request.user.id  # Получаем идентификатор пользователя
        user = get_object_or_404(User, id=user_id)  # Получаем пользователя по идентификатору

        # Если ответ правильный, помечаем is_correct как True
        is_correct = (answer == test.correct_answer)

        # Проверяем, проходил ли пользователь с данным идентификатором уже этот тест
        if TestResult.objects.filter(test=test, user=user).exists():
            # Если пользователь уже проходил тест, перенаправляем на список тестов текущего материала
            return HttpResponseRedirect(reverse('education:list_test', kwargs={'material_id': test.material.pk}))

        if answer:
            # Обработка правильного ответа
            test.testresult_set.create(user=user, choice=answer, is_correct=is_correct)
            material = test.material
            all_tests = Test.objects.filter(material=material).order_by('id')

        return HttpResponseRedirect(reverse('education:test_list', kwargs={'material_id': test.material.pk}))


class TestResultListView(ListView):  # Добавить LoginRequiredMixin, после прохождения тестов.
    """
    Контроллер списка результатов теста.
    """
    model = TestResult
    serializer_class = TestResultSerializer
    queryset = TestResult.objects.all()
    template_name = 'education/test_result_list.html'
    extra_context = {'title': 'Результаты теста'}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
