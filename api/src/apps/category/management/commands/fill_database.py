from django.core.management.base import BaseCommand
from category.models import Category
from page.models import Page
import random

class Command(BaseCommand):
    help = 'Fill the database with predefined categories, subcategories, and pages for leaf categories only'

    def handle(self, *args, **kwargs):
        # Удаляем все записи из базы данных
        Category.objects.all().delete()
        Page.objects.all().delete()

        # Определяем предустановленные категории с их ID
        categories_data = [
            {"name": "MMORPG", "id": 1},
            {"name": "MUD", "id": 2},
            {"name": "VR", "id": 3},
            {"name": "KIDS", "id": 4},
            {"name": "SOCIAL", "id": 5},
            {"name": "ART", "id": 6},
            {"name": "SANDBOX", "id": 7},
        ]

        # Создаем основные категории с заданными ID
        for category_data in categories_data:
            # Создаем родительскую категорию
            parent_category = Category.objects.create(
                id=category_data['id'],
                nameOfCategory=category_data['name'],
                countOfNestedWorld=0,
                flagForInternalRecordings=True,  # Флаг для внутренних записей
                flagForThePresenceOfAParent=False  # Флаг для отсутствия родителя
            )

            # Создаем подкатегории первого уровня
            for j in range(1, random.randint(2, 4)):  # 2-4 подкатегории первого уровня
                subcategory = Category.objects.create(
                    nameOfCategory=f"{category_data['name']} Subcategory {j}",
                    countOfNestedWorld=0,
                    parentCategory=parent_category,
                )

                # Создаем подкатегории второго уровня
                for k in range(1, random.randint(2, 4)):  # 2-4 подкатегории второго уровня
                    sub_subcategory = Category.objects.create(
                        nameOfCategory=f"{category_data['name']} Subcategory {j}.{k}",
                        countOfNestedWorld=0,
                        parentCategory=subcategory,
                    )

                    # Создаем подкатегории третьего уровня (если нужно)
                    for l in range(1, random.randint(2, 3)):  # 2-3 подкатегории третьего уровня
                        sub_sub_subcategory = Category.objects.create(
                            nameOfCategory=f"{category_data['name']} Subcategory {j}.{k}.{l}",
                            countOfNestedWorld=0,
                            parentCategory=sub_subcategory,
                        )

                        # Создаем страницы только для конечных категорий (с подкатегориями третьего уровня)
                        for page_num in range(1, random.randint(2, 4)):  # 2-3 страницы для каждой конечной категории
                            Page.objects.create(
                                nameOfPage=f"Page for {sub_sub_subcategory.nameOfCategory} {page_num}",
                                parentCategoryKey=sub_sub_subcategory
                            )

                    # Создаем страницы только для подкатегорий второго уровня, если это конечные категории
                    if not sub_subcategory.subcategories.exists():  # Это конечная категория второго уровня
                        for page_num in range(1, random.randint(2, 4)):  # 2-3 страницы
                            Page.objects.create(
                                nameOfPage=f"Page for {sub_subcategory.nameOfCategory} {page_num}",
                                parentCategoryKey=sub_subcategory
                            )

                # Создаем страницы только для подкатегорий первого уровня, если это конечные категории
                if not subcategory.subcategories.exists():  # Это конечная категория первого уровня
                    for page_num in range(1, random.randint(2, 4)):  # 2-3 страницы
                        Page.objects.create(
                            nameOfPage=f"Page for {subcategory.nameOfCategory} {page_num}",
                            parentCategoryKey=subcategory
                        )

            # Создаем страницы только для родительской категории, если она не имеет подкатегорий
            if not parent_category.subcategories.exists():  # Это конечная категория
                for page_num in range(1, random.randint(2, 4)):  # 2-3 страницы
                    Page.objects.create(
                        nameOfPage=f"Page for {parent_category.nameOfCategory} {page_num}",
                        parentCategoryKey=parent_category
                    )

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with predefined categories, subcategories, and pages for leaf categories only'))
