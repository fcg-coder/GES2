from django.test import TestCase  # Импортируем базовый класс TestCase для создания тестов
from category.models import Category  # Импортируем модель Category для использования в тестах
from page.models import Page


# #test_category_creation
# Проверяет, что категория создаётся с правильными значениями полей и флагов.

# test_link_child
# Проверяет корректное связывание дочерней категории с родительской и обновление флагов.

# test_flags_update_on_save
# Проверяет обновление флагов при сохранении категории.

# test_signal_post_save_updates_internal_recordings
# Проверяет, что сигнал обновляет флаг внутренних записей при добавлении дочерней категории.

# test_update_count_of_virtual_worlds_terminal_category
# Проверяет подсчёт миров для терминальной категории.

# test_update_count_of_virtual_worlds_with_subcategories
# Проверяет подсчёт миров для категории с подкатегориями.

# test_update_count_of_virtual_worlds_recursive
# Проверяет рекурсивное обновление миров на всех уровнях категорий. 
# 
class CategoryModelTest(TestCase):  # Определяем класс тестов для модели Category

    def setUp(self):
        self.parent_category = Category.objects.create(nameOfCategory='Родительская категория', flagForThePresenceOfAParent=False)
        self.child_category = Category.objects.create(nameOfCategory='Дочерняя категория', parentCategory=self.parent_category, flagForThePresenceOfAParent=True)
        self.terminal_category = Category.objects.create(nameOfCategory='Конечная категория', parentCategory=self.child_category, flagForThePresenceOfAParent=True)

    def test_category_creation(self):  # Тест для проверки создания категории
        """Проверка, что категория создается и сохраняется корректно"""  # Описание теста
        category = Category.objects.create(nameOfCategory='Тестовая категория', countOfNestedWorld=3)  # Создаём тестовую категорию
        self.assertEqual(category.nameOfCategory, 'Тестовая категория')  # Проверяем, что имя категории совпадает
        self.assertEqual(category.countOfNestedWorld, 3)  # Проверяем, что значение countOfNestedWorld равно 3
        self.assertFalse(category.flagForInternalRecordings)  # Проверяем, что флаг для внутренних записей равен False
        self.assertFalse(category.flagForThePresenceOfAParent)  # Проверяем, что флаг наличия родительской категории равен False

    def test_link_child(self):  # Тест для проверки связывания дочерней категории с родительской
        """Проверка, что дочерняя категория корректно связывается с родительской"""  # Описание теста
        
        # Проверяем, что у дочерней категории установлен родитель
        self.assertEqual(self.child_category.parentCategory, self.parent_category)  # Проверяем, что parentCategory дочерней категории совпадает с родительской

        # Проверяем, что у родителя добавлена дочерняя категория в childCategoies
        self.assertIn(self.child_category, self.parent_category.childCategoies.all())  # Проверяем, что дочерняя категория есть в childCategoies родителя

        # Проверяем, что флаг наличия подкатегорий обновился
        self.assertTrue(self.parent_category.flagForInternalRecordings)  # Проверяем, что флаг для внутренних записей родительской категории установлен в True

    def test_flags_update_on_save(self):  # Тест для проверки обновления флагов при сохранении категории
        """Проверка, что флаги обновляются при сохранении категории"""  # Описание теста
        self.child_category.parentCategory = self.parent_category  # Устанавливаем родителя для дочерней категории
        self.child_category.save()  # Сохраняем дочернюю категорию
        
        # Проверяем, что флаг наличия родительской категории установлен
        self.assertTrue(self.child_category.flagForThePresenceOfAParent)  # Проверяем, что флаг наличия родителя установлен в True

    def test_signal_post_save_updates_internal_recordings(self):  # Тест для проверки обновления флага наличия внутренних записей
        """Проверка, что сигнал post_save обновляет флаг наличия внутренних записей"""  # Описание теста
        # Добавляем дочернюю категорию вручную
        self.parent_category.childCategoies.add(self.child_category)  # Добавляем дочернюю категорию в childCategoies родительской категории
    
          # Проверяем, что сигнал обновил флаг наличия внутренних записей
        updated_parent_category = Category.objects.get(id=self.parent_category.id)  # Получаем обновлённый объект родительской категории из базы данных
        self.assertTrue(updated_parent_category.flagForInternalRecordings)  # Проверяем, что флаг для внутренних записей установлен в True

    def test_update_count_of_virtual_worlds_terminal_category(self):
        """Проверка расчёта миров для конечной категории"""
        Page.objects.create(nameOfPage='Страница 1', parentCategoryKey=self.terminal_category)
        Page.objects.create(nameOfPage='Страница 2', parentCategoryKey=self.terminal_category)
        
        self.terminal_category.update_count_of_virtual_worlds()
        self.assertEqual(self.terminal_category.countOfNestedWorld, 2)  # Проверяем, что подсчитано 2 мира

    def test_update_count_of_virtual_worlds_with_subcategories(self):
        """Проверка расчёта миров для категории с подкатегориями"""
        Page.objects.create(nameOfPage='Страница 1', parentCategoryKey=self.terminal_category)
        self.child_category.update_count_of_virtual_worlds()
        
        self.assertEqual(self.child_category.countOfNestedWorld, 1)  # Проверяем, что учтены миры дочерней категории
        
        self.parent_category.update_count_of_virtual_worlds()
        self.assertEqual(self.parent_category.countOfNestedWorld, 1)  # Проверяем, что учтены миры через подкатегории

    def test_update_count_of_virtual_worlds_recursive(self):
        """Проверка рекурсивного обновления миров"""
        Page.objects.create(nameOfPage='Страница 1', parentCategoryKey=self.terminal_category)
        
        self.terminal_category.update_count_of_virtual_worlds()
        self.child_category.update_count_of_virtual_worlds()
        self.parent_category.update_count_of_virtual_worlds()

        self.assertEqual(self.terminal_category.countOfNestedWorld, 1)  # Проверка на уровне терминальной категории
        self.assertEqual(self.child_category.countOfNestedWorld, 1)  # Проверка на уровне дочерней категории
        self.assertEqual(self.parent_category.countOfNestedWorld, 1)  # Проверка на уровне родительской категории
