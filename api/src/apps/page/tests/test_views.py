from django.test import TestCase, Client  # Импортируем классы для тестирования
from django.urls import reverse  # Импортируем функцию для получения URL-адресов по именам
from django.utils import timezone  # Импортируем модуль для работы с временными метками
from page.models import Page, Comment  # Импортируем модели Page и Comment из приложения page
from category.models import Category  # Импортируем модель Category из приложения category

class PageViewTests(TestCase):  # Определяем класс тестов для представлений страниц

    def setUp(self):  # Метод, который выполняется перед каждым тестом
        self.client = Client()  # Создаем клиент для тестирования запросов
        self.category = Category.objects.create(nameOfCategory='Test Category')  # Создаем тестовую категорию
        self.page = Page.objects.create(nameOfPage='Test Page', parentCategoryKey=self.category)  # Создаем тестовую страницу, привязанную к категории

        # Создаем комментарий для этой страницы
        self.comment = Comment.objects.create(
            username='testuser',  # Имя пользователя, оставляющего комментарий
            commentText='Test comment',  # Текст комментария
            ParentPageKey=self.page,  # Указываем страницу, к которой принадлежит комментарий
            publishedDate=timezone.now()  # Устанавливаем текущую дату и время публикации комментария
        )

    def test_index_page_exists(self):  # Тестируем существование страницы
        response = self.client.get(reverse('page:index', args=[self.page.id]))  # Выполняем GET-запрос к индексу страницы
        self.assertEqual(response.status_code, 200)  # Проверяем, что код состояния 200 (ОК)

    def test_index_page_not_found(self):  # Тестируем ситуацию, когда страница не найдена
        response = self.client.get(reverse('page:index', args=[999]))  # Выполняем GET-запрос к некорректному ID
        self.assertEqual(response.status_code, 404)  # Проверяем, что код состояния 404 (Не найдено)

    def test_leave_comment_empty_text(self):  # Тестируем оставление комментария с пустым текстом
        response = self.client.post(reverse('page:leave_comment', args=[self.page.id]), {
            'commentText': ''  # Убедитесь, что имя поля соответствует вашему полю в модели
        })
        self.assertEqual(response.status_code, 400)  # Предполагаем, что это код для неверного запроса

    def test_leave_comment_invalid_method(self):  # Тестируем недопустимый метод для оставления комментария
        response = self.client.get(reverse('page:leave_comment', args=[self.page.id]))  # Выполняем GET-запрос вместо POST
        self.assertEqual(response.status_code, 405)  # Код для "Метод не разрешен"

    def test_leave_comment_success(self):  # Тестируем успешное оставление комментария
        response = self.client.post(reverse('page:leave_comment', args=[self.page.id]), {
            'commentText': 'Test comment'  # Убедитесь, что имя поля соответствует вашему полю в модели
        })
        self.assertEqual(response.status_code, 201)  # Предполагаем, что это код для успешного создания ресурса
