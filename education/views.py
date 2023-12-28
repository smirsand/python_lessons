from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from rest_framework import request

from education.forms import TestForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_result_exists = TestResult.objects.filter(user=self.request.user).exists()
        context['is_passed'] = test_result_exists
        return context

    def post(self, request, *args, **kwargs):
        material_id = kwargs.get('material_id')
        test_id = int(request.POST.get('id'))
        test = get_object_or_404(Test, id=test_id)
        question = test.question
        answer = int(request.POST.get('answer', ''))
        is_correct = (answer == test.correct_answer)

        try:
            test = Test.objects.filter(question=question).first()
            TestResult.objects.create(user=request.user, test=test, choice=answer, is_correct=is_correct)
            return HttpResponseRedirect(reverse('education:test_list', args=[material_id]))
        except Exception as e:
            return HttpResponse(f'Ошибка: {e}')


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'education/test_detail.html'
    form_class = TestForm
    extra_context = {'title': 'Тест'}

    def get_object(self, queryset=None):
        order = self.kwargs.get('order')
        queryset = self.get_queryset()

        if order is not None:
            queryset = queryset.filter(order=order)

        return super().get_object(queryset)

    # def post(self, request, *args, **kwargs):
    #     test = get_object_or_404(Test, pk=kwargs['pk'])
    #     answer = int(request.POST.get('answer', ''))
    #     user = request.user
    #
    #     # Получаем идентификатор материала
    #     material_id = test.material.id
    #
    #     # Если ответ правильный, помечаем is_correct как True
    #     is_correct = (answer == test.correct_answer)
    #
    #     if answer:
    #         test.testresult_set.create(user=user, choice=answer, is_correct=is_correct)
    #
    #     # Найти следующий тест материала
    #     next_test = Test.objects.filter(material_id=material_id, order__gt=test.order).first()
    #
    #     if next_test:
    #         return redirect('education:test_detail', pk=next_test.id)
    #     else:
    #         # Если это был последний тест материала, перенаправить пользователя на страницу с материалом
    #         return redirect('education:material_detail', pk=material_id)


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
