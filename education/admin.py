from django.contrib import admin

from education.models import Chapter, Material, Test, Answer


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
    list_display = ('question',)  # Вывод столбцов в таблице
    list_filter = ('question',)  # Фильтрация
    search_fields = ('question',)  # Поиск


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('test', 'text', 'is_correct')  # Вывод столбцов в таблице
    list_filter = ('text', 'test', 'is_correct',)  # Фильтрация
    search_fields = ('text', 'test', 'is_correct',)  # Поиск