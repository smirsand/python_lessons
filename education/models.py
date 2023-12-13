from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Chapter(models.Model):
    """
    Модель учебного раздела.
    """
    name_chapter = models.CharField(max_length=100, verbose_name='наименование раздела')
    description_chapter = models.TextField(verbose_name='описание раздела', **NULLABLE)

    def __str__(self):
        return f'{self.name_chapter}'

    class Meta:
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'


class Materials(models.Model):
    """
    Модель учебного материала.
    """
    name_material = models.CharField(max_length=255, verbose_name='название')
    description_material = models.TextField(verbose_name='описание')
    video_link_material = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='раздел')

    def __str__(self):
        return f'{self.name_material}'

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
