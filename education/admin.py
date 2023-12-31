from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import F

from education.models import Chapter, Material, Test, TestResult


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    """
    Класс для настройки администраторской панели модели Chapter.
    """
    list_display = ('name_chapter',)  # Вывод столбцов в таблице
    list_filter = ('name_chapter',)  # Фильтрация
    search_fields = ('name_chapter',)  # Поиск


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """
    Класс для настройки администраторской панели модели Material.
    """
    list_display = ('name_material', 'chapter',)  # Вывод столбцов в таблице
    list_filter = ('name_material', 'chapter',)  # Фильтрация
    search_fields = ('name_material',)  # Поиск


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """
    Класс для настройки администраторской панели модели Test.
    """
    list_display = ('question', 'material', 'get_material_chapter', 'correct_answer',)  # Вывод столбцов в таблице
    list_filter = ('material',)  # Фильтрация
    search_fields = ('question',)  # Поиск

    def get_material_chapter(self, obj):
        return obj.material.chapter

    get_material_chapter.short_description = 'раздел'


class CorrectAnswerFilter(SimpleListFilter):
    """
    Фильтр административной панели для отображения объектов модели на основе правильного ответа на тестовый вопрос.
    """
    title = 'правильный ответ'
    parameter_name = 'correct_answer'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':  # Если значение 'yes', метод возвращает объекты, 'choice' = 'correct_answer'.
            return queryset.filter(choice=F('test__correct_answer'))
        elif self.value() == 'no':
            return queryset.exclude(choice=F('test__correct_answer'))
        else:
            return queryset


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    """
    Класс для настройки администраторской панели модели TestResult.
    """
    list_display = ('date', 'user', 'test', 'material', 'choice', 'correct_answer')  # Вывод столбцов в таблице
    list_filter = ('date', 'user', CorrectAnswerFilter)  # Фильтрация
    search_fields = ('user',)  # Поиск

    def correct_answer(self, obj):  # Функция является методом модели для получения значения "правильного ответа".
        test = getattr(obj, 'test', None)
        if test:
            correct_answer = test.correct_answer
            return correct_answer
        return None

    correct_answer.short_description = 'правильный ответ'

    def material(self, obj):  # Функция является методом модели для получения значения "материала".
        test = getattr(obj, 'test', None)
        if test:
            material = test.material
            return material
        return None

    material.short_description = 'материал'
