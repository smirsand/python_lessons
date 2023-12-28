from django.contrib import admin

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


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'test', 'material', 'choice', 'correct_answer')  # Вывод столбцов в таблице
    list_filter = ('date',)  # Фильтрация
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