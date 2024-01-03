from time import sleep

from rest_framework import status
from rest_framework.test import APITestCase

from education.models import TestResult, Test, Material, Chapter
from users.models import User


class TestResultCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(email='test@mail.ru', password='test', first_name='Test', last_name='Testov',
                                        is_staff=True, is_superuser=True, is_active=True)
        self.client.force_authenticate(user=self.user)
        self.chapter = Chapter.objects.create(name_chapter="Раздел")
        self.material = Material.objects.create(name_material="Материал", description_material="Описание",
                                                chapter=self.chapter)
        self.material_id = Material.objects.get(pk=self.material.id)
        self.test = Test.objects.create(question="Сколько ног у стула?", material=self.material_id, correct_answer=1)
        self.test_pk = Test.objects.get(pk=1)
        # print(self.test_pk)
        self.user_id = User.objects.get(pk=1)  # Получаем экземпляр пользователя по его идентификатору

    def test_test_result_list(self):
        """Тест получения списка результатов"""

        self.client.force_login(self.user)  # аутентификация пользователя.

        data = {
            "test": self.test_pk,
            "is_correct": True,
            "choice": 1,
        }
        # Создается и сохраняется объект TestResult на основе данных.
        result = TestResult(**data)
        result.save()

        # print("Результат сохранения:", result.test, result.is_correct, result.id)

        # Получение списка результатов
        response = self.client.get('/result_list/')

        print(response)

        # Проверяем статус код получения списка результатов
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Все объекты TestResult из базы данных
        results = TestResult.objects.all()

        # Полученные результаты
        for result in results:
            test = result.test
            is_correct = result.is_correct
            choice = result.choice

            # Полученные данные
            print(f"Тест: {test}, Правильный ли ответ: {is_correct}, Выбор: {choice}")

        # self.assertEqual(
        #     response.headers['Content-Type'],
        #     'application/json'
        # )
        #
        # response = self.client.get('/result_list/')
        #
        # self.assertEqual(response.json(), {
        #     "id": 31,
        #     "is_correct": True,
        #     "choice": 2,
        #     "date": "2023-12-29T21:32:17.901406+03:00",
        #     "user": 1,
        #     "test": 1
        # }
        #                  )
        #
        # self.assertTrue(
        #     TestResult.objects.all().exists()
        # )
