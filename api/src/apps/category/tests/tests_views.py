from django.test import TestCase, Client  # Импортируем классы для тестирования
from django.urls import reverse  # Импортируем функцию для получения URL по имени
from category.models import Category  # Импортируем модель Category

class CategoryViewTests(TestCase):  # Определяем класс тестов для представлений категории
    def setUp(self):
        self.client = Client()  # Создаем клиент для тестирования запросов
        # Создаем тестовые категории для использования в тестах
        self.category1 = Category.objects.create(
            nameOfCatergory="Category 1",  # Имя первой категории
            countOfNestedWorld=5,  # Количество миров для первой категории
            flagForThePresenceOfAParent=False  # Флаг для родительской категории
        )
        self.category2 = Category.objects.create(
            nameOfCatergory="Category 2",  # Имя второй категории
            countOfNestedWorld=10,  # Количество миров для второй категории
            flagForThePresenceOfAParent=False  # Флаг для родительской категории
        )

    def test_index_view(self):
        response = self.client.get(reverse('category:index'))  # Выполняем GET-запрос к представлению индекса
        self.assertEqual(response.status_code, 200)  # Проверяем, что статус ответа 200 (успех)
        
        # Проверяем, что в возвращаемых данных есть ключ "categories"
        data = response.json()
        self.assertIn("categories", data)
        self.assertEqual(len(data["categories"]), 2)  # Ожидаем 2 категории

        # Проверяем данные для каждой категории
        self.assertEqual(data["categories"][0]["nameOfCatergory"], "Category 1")  # Проверяем имя первой категории
        self.assertEqual(data["categories"][1]["nameOfCatergory"], "Category 2")  # Проверяем имя второй категории
        
        # Здесь можно добавить проверку других атрибутов, если необходимо
        
    def test_index_view_no_categories(self):
        Category.objects.all().delete()  # Удаляем все категории для тестирования пустого состояния
        response = self.client.get(reverse('category:index'))  # Выполняем запрос снова
        self.assertEqual(response.status_code, 200)  # Проверяем статус ответа
        data = response.json()  # Получаем данные из ответа
        self.assertIn("categories", data)  # Проверяем наличие ключа "categories"
        self.assertEqual(data["categories"], [])  # Ожидаем пустой список категорий
