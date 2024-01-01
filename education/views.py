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

    def get_context_data(self, **kwargs):  # для получения дополнительных контекстных данных для передачи в шаблон.
        context = super().get_context_data(**kwargs)
        test = self.get_object()
        user = self.request.user
        context['tests'] = [{
            'test': test,
            'completed': TestResult.objects.filter(test=test, user=user).exists()
        }]
        return context

    def post(self, request, *args, **kwargs):
        # получаем объект теста по его первичному ключу (pk).
        test = get_object_or_404(Test, pk=kwargs['pk'])
        # получаем значение ответа из POST-запроса.
        answer = int(request.POST.get('answer', ''))
        # получаем идентификатор пользователя
        user_id = request.user.id
        # получаем пользователя по идентификатору
        user = get_object_or_404(User, id=user_id)

        # сравниваем полученный ответ, если ответ правильный, помечаем is_correct как True
        is_correct = (answer == test.correct_answer)

        # проверяем, был ли получен ответ на вопрос.
        if answer:
            # создаем объект TestResult
            test.testresult_set.create(user=user, choice=answer, is_correct=is_correct)
            # получаем объект материала, к которому относится данный тест.
            material = test.material
            # получаем все тесты для данного материала и сортируем их по полю id
            Test.objects.filter(material=material).order_by('id')

            # Перенаправляем пользователя на страницу списка тестов для данного материала.
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
        # получаем базовый набор объектов из родительского класса ListView.
        queryset = super().get_queryset()
        # фильтруем объекты, оставляя те, которые принадлежат текущему пользователю.
        queryset = queryset.filter(user=self.request.user)
        return queryset
