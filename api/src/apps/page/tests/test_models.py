from django.test import TestCase  # Импортируем класс TestCase для создания тестов
from page.models import Page, Comment  # Импортируем модели Page и Comment из приложения page
from category.models import Category  # Импортируем модель Category из приложения category
from django.utils import timezone  # Импортируем модуль для работы с временными метками

class PageModelTest(TestCase):  # Определяем класс тестов для модели страницы

    @classmethod
    def setUpTestData(cls):  # Метод, который выполняется один раз для настройки данных перед тестами
        # Создание родительской категории
        cls.category = Category.objects.create(nameOfCategory='Test Category')  # Создаем тестовую категорию

        # Создание объекта Page
        cls.page = Page.objects.create(
            nameOfPage='Test Page',  # Имя страницы
            reviewStatus='pending',  # Статус рецензии
            tagTextBasedMMOs='MUD',  # Тег для текстовых MMO
            tagGraphicalMMOs='MMORPG',  # Тег для графических MMO
            parentCategoryKey=cls.category  # Указываем родительскую категорию
        )

    def test_page_creation(self):  # Тестируем создание страницы
        """Тест на создание страницы"""
        self.assertEqual(self.page.nameOfPage, 'Test Page')  # Проверяем, что имя страницы соответствует ожидаемому
        self.assertEqual(self.page.reviewStatus, 'pending')  # Проверяем, что статус рецензии соответствует ожидаемому
        self.assertEqual(self.page.tagTextBasedMMOs, 'MUD')  # Проверяем, что тег текстовых MMO соответствует ожидаемому
        self.assertEqual(self.page.tagGraphicalMMOs, 'MMORPG')  # Проверяем, что тег графических MMO соответствует ожидаемому
        self.assertEqual(self.page.parentCategoryKey, self.category)  # Проверяем, что родительская категория соответствует ожидаемой

    def test_page_string_representation(self):  # Тестируем строковое представление страницы
        """Тест на строковое представление страницы"""
        self.assertEqual(str(self.page), 'Test Page')  # Проверяем, что строковое представление соответствует ожидаемому

class CommentModelTest(TestCase):  # Определяем класс тестов для модели комментария

    @classmethod
    def setUpTestData(cls):  # Метод, который выполняется один раз для настройки данных перед тестами
        # Создание родительской категории и страницы
        cls.category = Category.objects.create(nameOfCategory='Test Category')  # Создаем тестовую категорию
        cls.page = Page.objects.create(
            nameOfPage='Test Page',  # Имя страницы
            reviewStatus='pending',  # Статус рецензии
            tagTextBasedMMOs='MUD',  # Тег для текстовых MMO
            tagGraphicalMMOs='MMORPG',  # Тег для графических MMO
            parentCategoryKey=cls.category  # Указываем родительскую категорию
        )

        # Создание объекта Comment
        cls.comment = Comment.objects.create(
            commentText='Test Comment',  # Текст комментария
            publishedDate=timezone.now(),  # Устанавливаем текущую дату и время публикации комментария
            ParentPageKey=cls.page,  # Указываем страницу, к которой принадлежит комментарий
            username='TestUser'  # Имя пользователя, оставляющего комментарий
        )

    def test_comment_creation(self):  # Тестируем создание комментария
        """Тест на создание комментария"""
        self.assertEqual(self.comment.commentText, 'Test Comment')  # Проверяем, что текст комментария соответствует ожидаемому
        self.assertEqual(self.comment.username, 'TestUser')  # Проверяем, что имя пользователя соответствует ожидаемому
        self.assertEqual(self.comment.ParentPageKey, self.page)  # Проверяем, что родительская страница соответствует ожидаемой

    def test_comment_string_representation(self):  # Тестируем строковое представление комментария
        """Тест на строковое представление комментария"""
        self.assertEqual(str(self.comment), 'Test Comment')  # Проверяем, что строковое представление соответствует ожидаемому
