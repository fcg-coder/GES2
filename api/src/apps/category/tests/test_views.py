from django.test import TestCase, Client  # Импортируем классы для тестирования
from django.urls import reverse  # Импортируем функцию для получения URL по имени
from category.models import Category  # Импортируем модель Category
from page.models import Page  # Импортируем модель Page
import networkx as nx  # Импортируем библиотеку для работы с графами

class CategoryViewTests(TestCase):  # Определяем класс тестов для представлений категории
    def setUp(self):
        self.client = Client()  # Создаем клиент для тестирования запросов
        # Создаем тестовые категории для использования в тестах
        self.category1 = Category.objects.create(
            nameOfCategory="Category 1",  # Имя первой категории
            countOfNestedWorld=5,  # Количество миров для первой категории
            flagForThePresenceOfAParent=0  # Флаг для родительской категории
        )
        self.category2 = Category.objects.create(
            nameOfCategory="Category 2",  # Имя второй категории
            countOfNestedWorld=10,  # Количество миров для второй категории
            flagForThePresenceOfAParent=0  # Флаг для родительской категории
        )

    def test_index_view(self):
        response = self.client.get(reverse('category:index'))  # Выполняем GET-запрос к представлению индекса
        self.assertEqual(response.status_code, 200)  # Проверяем, что статус ответа 200 (успех)
        
        # Проверяем, что в возвращаемых данных есть ключ "categories"
        data = response.json()
        self.assertIn("categories", data)
        self.assertEqual(len(data["categories"]), 2)  # Ожидаем 2 категории

        # Проверяем данные для каждой категории
        self.assertEqual(data["categories"][0]["nameOfCategory"], "Category 1")  # Проверяем имя первой категории
        self.assertEqual(data["categories"][1]["nameOfCategory"], "Category 2")  # Проверяем имя второй категории
        
    def test_index_view_no_categories(self):
        Category.objects.all().delete()  # Удаляем все категории для тестирования пустого состояния
        response = self.client.get(reverse('category:index'))  # Выполняем запрос снова
        self.assertEqual(response.status_code, 200)  # Проверяем статус ответа
        data = response.json()  # Получаем данные из ответа
        self.assertIn("categories", data)  # Проверяем наличие ключа "categories"
        self.assertEqual(data["categories"], [])  # Ожидаем пустой список категорий



"""
Тест проверяет представление графа, создавая тестовые категории и страницы.
- В setUp создаются категории и страницы.
- В test_graph_view отправляется GET-запрос, ожидая узлы и ребра:
  - Узлы: 'Category 1', 'Subcategory 1', 'Category 2', 'Page 1', 'Page 2'.
  - Ребра: связи между категориями и страницами.
"""

class GraphViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.category1 = Category.objects.create(
            nameOfCategory="Category 1",
            countOfNestedWorld=0,
            flagForThePresenceOfAParent=False,
            flagForInternalRecordings=True
        )

        self.subcategory1 = Category.objects.create(
            nameOfCategory="Subcategory 1",
            countOfNestedWorld=0,
            flagForThePresenceOfAParent=True
        )
        self.category1.internalPages.add(self.subcategory1)  # Связываем подкатегорию с категорией

        self.category2 = Category.objects.create(
            nameOfCategory="Category 2",
            countOfNestedWorld=0,
            flagForThePresenceOfAParent=False
        )
        self.page1 = Page.objects.create(nameOfPage="Page 1", parentCategoryKey=self.category2)
        self.page2 = Page.objects.create(nameOfPage="Page 2", parentCategoryKey=self.category2)

    def test_graph_view(self):
        response = self.client.get(reverse('category:graph'))
        data = response.json()

        expected_nodes = [
            {'id': 1, 'label': 'Category 1'},
            {'id': 2, 'label': 'Subcategory 1'},
            {'id': 3, 'label': 'Category 2'},
            {'id': 'page_1', 'label': 'Page 1'},
            {'id': 'page_2', 'label': 'Page 2'},
        ]
        
        self.assertEqual(
            sorted(data["nodes"], key=lambda x: str(x['id'])),
            sorted(expected_nodes, key=lambda x: str(x['id']))
        )
        
        expected_edges = [
            {'from': 1, 'to': 2},  # связь между Category 1 и Subcategory 1
            {'from': 3, 'to': 'page_1'},  # связь между Category 2 и Page 1
            {'from': 3, 'to': 'page_2'}   # связь между Category 2 и Page 2
        ]
        
        self.assertEqual(
            sorted(data["edges"], key=lambda x: (x['from'], x['to'])),
            sorted(expected_edges, key=lambda x: (x['from'], x['to']))
        )



    def test_graph_view_no_categories(self):
        Category.objects.all().delete()  # Удаляем все категории для тестирования пустого состояния
        Page.objects.all().delete()  # Удаляем все страницы
        response = self.client.get(reverse('category:graph'))  # Выполняем запрос снова
        self.assertEqual(response.status_code, 200)  # Проверяем статус ответа

        data = response.json()  # Получаем данные из ответа
        self.assertIn("nodes", data)  # Проверяем наличие ключа "nodes"
        self.assertIn("edges", data)  # Проверяем наличие ключа "edges"
        self.assertEqual(data["nodes"], [])  # Ожидаем пустой список узлов
        self.assertEqual(data["edges"], [])  # Ожидаем пустой список рёбер
