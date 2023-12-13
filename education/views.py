from django.views.generic import ListView, DetailView

from education.models import Chapter, Materials


class ChapterListView(ListView):
    model = Chapter
    template_name = 'education/home.html'
    extra_context = {'title': 'Главная'}


class ChapterDetailView(DetailView):
    model = Chapter
    template_name = 'education/education_detail.html'
    extra_context = {'title': 'Материалы раздела'}


class MaterialsListView(ListView):
    model = Materials
    template_name = 'education/education_detail.html'

    def get_queryset(self):
        chapter_id = self.kwargs['pk']
        return Materials.objects.filter(chapter_id=chapter_id)
