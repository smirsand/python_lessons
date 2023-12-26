from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Chapter(models.Model):
    """
    Модель учебного раздела.
    """
    name_chapter = models.CharField(max_length=100, verbose_name='наименование раздела')

    def __str__(self):
        return f'{self.name_chapter}'

    class Meta:
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'


class Material(models.Model):
    """
    Модель учебного материала.
    """
    name_material = models.CharField(max_length=255, verbose_name='название')
    description_material = models.TextField(verbose_name='описание')
    video_link_material = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='раздел')

    def __str__(self):
        return f'{self.name_material}, {self.chapter}'

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'


class Test(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='материал')
    question = models.TextField(verbose_name='вопрос')
    answer_1 = models.CharField(max_length=100, verbose_name='Ответ 1', default=0)
    answer_2 = models.CharField(max_length=100, verbose_name='Ответ 2', default=0)
    answer_3 = models.CharField(max_length=100, verbose_name='Ответ 3', default=0)
    correct_answer = models.IntegerField(choices=((1, 'Ответ 1'), (2, 'Ответ 2'), (3, 'Ответ 3')), default=0,
                                         verbose_name='Правильный ответ')

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='тест')
    choice = models.IntegerField(verbose_name='выбор')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата')

    def __str__(self):
        return f'{self.user}, {self.test}, {self.choice}'

    class Meta:
        verbose_name = 'результат теста'
        verbose_name_plural = 'результаты тестов'
