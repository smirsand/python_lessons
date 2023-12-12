from django.contrib import admin

from education.models import Chapter, Materials


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name_chapter', 'description_chapter',)  # Вывод столбцов в таблице
    list_filter = ('name_chapter',)  # Фильтрация
    search_fields = ('name_chapter',)  # Поиск


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('name_material', 'description_material',)  # Вывод столбцов в таблице
    list_filter = ('name_material',)  # Фильтрация
    search_fields = ('name_material',)  # Поиск
