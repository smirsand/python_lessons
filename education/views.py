from django.views.generic import ListView, DetailView

from education.models import Chapter, Material, Test


class ChapterListView(ListView):
    model = Chapter
    template_name = 'education/home.html'
    extra_context = {'title': 'Главная'}


class ChapterDetailView(DetailView):
    model = Chapter
    template_name = 'education/education_detail.html'
    extra_context = {'title': 'Материалы раздела'}


class MaterialListView(ListView):
    model = Material
    template_name = 'education/education_detail.html'
    extra_context = {'title': 'Список материалов раздела'}

    def get_queryset(self):
        chapter_id = self.kwargs['pk']
        return Material.objects.filter(chapter_id=chapter_id)


class MaterialDetailView(DetailView):
    model = Material
    template_name = 'education/material_detail.html'
    extra_context = {'title': 'Материал'}


class TestListView(ListView):
    model = Test
    template_name = 'education/test_list.html'
    extra_context = {'title': 'Тесты'}
