from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Test, Material, Chapter, TestResult
from users.models import User


class TestResultCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(email='test@mail.ru', password='test', first_name='Test', last_name='Testov',
                                        is_staff=True, is_superuser=True, is_active=True)
        self.chapter = Chapter.objects.create(name_chapter="Раздел")
        self.material = Material.objects.create(name_material="Материал", description_material="Описание",
                                                chapter=self.chapter)
        self.material_id = Material.objects.get(pk=self.material.id)
        self.test = Test.objects.create(question="Сколько ног у стула?", material=self.material_id, correct_answer=1)
        self.test_pk = Test.objects.get(pk=1)

    def test_test_result_list(self):
        """Тест получения списка результатов"""

        self.client.force_login(self.user)  # аутентификация пользователя.

        data = {
            "test": self.test_pk.id,
            "is_correct": True,
            "choice": 1,
        }

        # Создается и сохраняется объект TestResult на основе данных.
        res = self.client.post('/result/create/', data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        print(res)

        # Получение списка результатов
        response = self.client.get(f'/results_list/{self.test_pk.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {
            'id': 1,
            'is_correct': True,
            'choice': 1,
            'date': res.json().get('date'),
            'user': None,
            'test': 1,
        })

        self.assertTrue(
            TestResult.objects.all().exists()
        )


class ChapterCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(email='test@mail.ru', password='test', first_name='Test', last_name='Testov',
                                        is_staff=True, is_superuser=True, is_active=True)
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        self.chapter = Chapter.objects.create(name_chapter="Раздел")

    def test_chapter_retrieve(self):
        """Тест получения раздела"""

        self.client.force_login(self.user)  # аутентификация пользователя.

        data = {
            "name_chapter": "Раздел №1",
        }

        # Создается и сохраняется объект Chapter на основе данных.
        res = self.client.post('/chapter/create/', data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Получение списка результатов
        response = self.client.get(f'/chapter_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), [{
                    'id': 1, 'name_chapter': 'Раздел'},
            {
                    'id': 2, 'name_chapter': 'Раздел №1'
                    }])

        self.assertTrue(
            Chapter.objects.all().exists()
        )
