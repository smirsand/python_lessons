from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import F

from education.models import Chapter, Material, Test, TestResult


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name_chapter',)  # Вывод столбцов в таблице
    list_filter = ('name_chapter',)  # Фильтрация
    search_fields = ('name_chapter',)  # Поиск


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name_material', 'chapter',)  # Вывод столбцов в таблице
    list_filter = ('name_material', 'chapter',)  # Фильтрация
    search_fields = ('name_material',)  # Поиск


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('question', 'material', 'get_material_chapter', 'correct_answer',)  # Вывод столбцов в таблице
    list_filter = ('question',)  # Фильтрация
    search_fields = ('question',)  # Поиск

    def get_material_chapter(self, obj):
        return obj.material.chapter

    get_material_chapter.short_description = 'раздел'


class CorrectAnswerFilter(SimpleListFilter):
    title = 'правильный ответ'
    parameter_name = 'correct_answer'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(choice=F('test__correct_answer'))
        elif self.value() == 'no':
            return queryset.exclude(choice=F('test__correct_answer'))
        else:
            return queryset


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'test', 'material', 'choice', 'correct_answer')  # Вывод столбцов в таблице
    list_filter = ('date', 'user', CorrectAnswerFilter)  # Фильтрация
    search_fields = ('user',)  # Поиск

    def correct_answer(self, obj):
        test = getattr(obj, 'test', None)
        if test:
            correct_answer = test.correct_answer
            return correct_answer
        return None

    correct_answer.short_description = 'правильный ответ'

    def material(self, obj):
        test = getattr(obj, 'test', None)
        if test:
            material = test.material
            return material
        return None

    material.short_description = 'материал'
