from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from education.forms import TestResultForm, TestForm
from education.models import Chapter, Material, Test, TestResult


class ChapterListView(ListView):
    model = Chapter
    template_name = 'education/home.html'
    extra_context = {'title': 'Главная'}


class ChapterDetailView(DetailView):
    model = Chapter
    template_name = 'education/materials_list.html'
    extra_context = {'title': 'Материалы раздела'}


class MaterialListView(ListView):
    model = Material
    template_name = 'education/materials_list.html'
    extra_context = {'title': 'Список материалов раздела'}

    def get_queryset(self):
        chapter_id = self.kwargs['pk']
        return Material.objects.filter(chapter_id=chapter_id)


class MaterialDetailView(DetailView):
    model = Material
    template_name = 'education/material_detail.html'
    extra_context = {'title': 'Материал'}


# @login_required
class TestDetailView(DetailView):
    model = Test
    form_class = TestForm
    template_name = 'education/test_detail.html'
    extra_context = {'title': 'Тест'}

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TestResultForm()
        return context

    def post(self, request, *args, **kwargs):
        test_id = kwargs['pk']
        test = self.get_object()
        answer = request.POST.get('answer', '')
        user = request.user
        TestResult.objects.create(user=user, test=test, choice=answer)
        next_tests = Test.objects.filter(order__gt=test.order).order_by('order')
        next_test = next_tests.first()

        if next_test:
            return HttpResponseRedirect(reverse('education:test_detail', args=[next_test.pk]))
        else:
            return HttpResponseRedirect(reverse('education:list_chapter'))
