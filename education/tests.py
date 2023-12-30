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
        self.test = Test.objects.create(question="Вопрос", material=self.material_id, correct_answer=1)
        self.test = Test.objects.get(pk=1)
        self.user_id = User.objects.get(pk=1)  # Получаем экземпляр пользователя по его идентификатору

    def test_test_result_list(self):
        """Тест получения списка результатов"""

        self.client.force_login(self.user)

        data = {
            "test": self.test,
            "is_correct": True,
            "choice": 1,
        }
        # Создание объекта
        result = TestResult(**data)
        result.save()

        # Получение списка результатов
        response = self.client.get('/result_list/')

        # Проверяем статус код получения списка результатов
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.headers['Content-Type'],
            'application/json'
        )

        self.assertEqual(response.json(), {
            "id": 31,
            "is_correct": True,
            "choice": 2,
            "date": "2023-12-29T21:32:17.901406+03:00",
            "user": 1,
            "test": 1
        }
                         )

        self.assertTrue(
            TestResult.objects.all().exists()
        )
