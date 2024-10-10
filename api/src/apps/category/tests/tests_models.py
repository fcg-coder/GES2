from django.test import TestCase  # Импортируем базовый класс TestCase для создания тестов
from category.models import Category  # Импортируем модель Category для использования в тестах

class CategoryModelTest(TestCase):  # Определяем класс тестов для модели Category
    def setUp(self):  # Метод, который выполняется перед каждым тестом
        # Создаём несколько категорий для тестов
        self.parent_category = Category.objects.create(nameOfCatergory='Родительская категория')  # Создаём родительскую категорию
        self.child_category = Category.objects.create(nameOfCatergory='Дочерняя категория')  # Создаём дочернюю категорию

    def test_category_creation(self):  # Тест для проверки создания категории
        """Проверка, что категория создается и сохраняется корректно"""  # Описание теста
        category = Category.objects.create(nameOfCatergory='Тестовая категория', countOfNestedWorld=3)  # Создаём тестовую категорию
        self.assertEqual(category.nameOfCatergory, 'Тестовая категория')  # Проверяем, что имя категории совпадает
        self.assertEqual(category.countOfNestedWorld, 3)  # Проверяем, что значение countOfNestedWorld равно 3
        self.assertFalse(category.flagForInternalRecordings)  # Проверяем, что флаг для внутренних записей равен False
        self.assertFalse(category.flagForThePresenceOfAParent)  # Проверяем, что флаг наличия родительской категории равен False

    def test_link_child(self):  # Тест для проверки связывания дочерней категории с родительской
        """Проверка, что дочерняя категория корректно связывается с родительской"""  # Описание теста
        self.parent_category.link_child(self.child_category)  # Связываем дочернюю категорию с родительской
        
        # Проверяем, что у дочерней категории установлен родитель
        self.assertEqual(self.child_category.parentPage, self.parent_category)  # Проверяем, что parentPage дочерней категории совпадает с родительской

        # Проверяем, что у родителя добавлена дочерняя категория в internalPages
        self.assertIn(self.child_category, self.parent_category.internalPages.all())  # Проверяем, что дочерняя категория есть в internalPages родителя

        # Проверяем, что флаг наличия подкатегорий обновился
        self.assertTrue(self.parent_category.flagForInternalRecordings)  # Проверяем, что флаг для внутренних записей родительской категории установлен в True

    def test_flags_update_on_save(self):  # Тест для проверки обновления флагов при сохранении категории
        """Проверка, что флаги обновляются при сохранении категории"""  # Описание теста
        self.child_category.parentPage = self.parent_category  # Устанавливаем родителя для дочерней категории
        self.child_category.save()  # Сохраняем дочернюю категорию
        
        # Проверяем, что флаг наличия родительской категории установлен
        self.assertTrue(self.child_category.flagForThePresenceOfAParent)  # Проверяем, что флаг наличия родителя установлен в True

    def test_signal_post_save_updates_internal_recordings(self):  # Тест для проверки обновления флага наличия внутренних записей
        """Проверка, что сигнал post_save обновляет флаг наличия внутренних записей"""  # Описание теста
        # Добавляем дочернюю категорию вручную
        self.parent_category.internalPages.add(self.child_category)  # Добавляем дочернюю категорию в internalPages родительской категории
        self.parent_category.link_child(self.child_category)  # Вызываем метод связывания дочерней категории с родительской

        # Проверяем, что сигнал обновил флаг наличия внутренних записей
        updated_parent_category = Category.objects.get(id=self.parent_category.id)  # Получаем обновлённый объект родительской категории из базы данных
        self.assertTrue(updated_parent_category.flagForInternalRecordings)  # Проверяем, что флаг для внутренних записей установлен в True
