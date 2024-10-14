from django.test import TestCase  # Импортируем базовый класс TestCase для создания тестов
from category.models import Category  # Импортируем модель Category для использования в тестах
from page.models import Page  # Импортируем модель Page для использования в тестах
import random


class CategoryModelTest(TestCase):  # Определяем класс тестов для модели Category

    def setUp(self):
        # Удаляем все записи из базы данных
        Category.objects.all().delete()
        Page.objects.all().delete()

        # Создаем родительскую категорию
        self.parent_category_count_if_nested_worlds_for_test = 0
        parent_category = Category.objects.create(
            nameOfCategory="Parent Category",
            countOfNestedWorld=0,
        )
        
        self.parent_categories = [parent_category]

        # Создаем случайное количество подкатегорий для родительской категории от 2 до 8
        for j in range(1, random.randint(2, 8)):  # 2-8 подкатегорий
            subcategory = Category.objects.create(
                nameOfCategory=f"Subcategory {j}",
                countOfNestedWorld=0,
                parentCategory=parent_category,
            )

            # Создаем случайное количество подкатегорий второго уровня от 2 до 8
            for k in range(1, random.randint(2, 8)):  # 2-8 подкатегорий второго уровня
                sub_subcategory = Category.objects.create(
                    nameOfCategory=f"Subcategory {j}.{k}",
                    countOfNestedWorld=0,
                    parentCategory=subcategory,
                )

                # Создаем случайное количество страниц для каждой конечной подкатегории от 2 до 8
                for page_num in range(1, random.randint(2, 8)):  # 2-8 страниц для каждой конечной категории
                    Page.objects.create(
                        nameOfPage=f"Page for {sub_subcategory.nameOfCategory} {page_num}",
                        parentCategoryKey=sub_subcategory
                    )
                    self.parent_category_count_if_nested_worlds_for_test += 1   

    def test_update_count_of_virtual_worlds_recursive(self):
        """Проверка рекурсивного обновления миров"""
        for parent in self.parent_categories:
    
            # Проверяем, что значение количества миров совпадает с ожидаемым
            # print(parent.countOfNestedWorld)
            # print(self.parent_category_count_if_nested_worlds_for_test)
            self.assertEqual(parent.countOfNestedWorld, self.parent_category_count_if_nested_worlds_for_test)  # Убедитесь, что значение равно ожидаемому
