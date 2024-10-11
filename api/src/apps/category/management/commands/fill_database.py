from django.core.management.base import BaseCommand
from category.models import Category
from page.models import Page
import random

class Command(BaseCommand):
    help = 'Fill the database with sample data'

    def handle(self, *args, **kwargs):
        # Удаляем все записи из базы данных
        Category.objects.all().delete()
        Page.objects.all().delete()

        # Создаем 2 родительские категории
        parent_categories = []
        for i in range(1, random.randint(2, 3)):  # 2-8 подкатегорий
            parent_category = Category.objects.create(
                nameOfCategory=f"Parent Category {i}",
                countOfNestedWorld=0,
                

            )
            parent_categories.append(parent_category)

            # Создаем несколько подкатегорий для каждой родительской категории
            for j in range(1, random.randint(2, 8)):  # 3 подкатегории
                subcategory = Category.objects.create(
                    nameOfCategory=f"Subcategory {i}.{j}",
                    countOfNestedWorld=0,
                    parentCategory = parent_category,
                )
                
                # Связываем подкатегорию с родительской категорией


                # Создаем подкатегории второго уровня
                for k in range(1, random.randint(2, 8)):  # 2 подкатегории второго уровня
                    sub_subcategory = Category.objects.create(
                        nameOfCategory=f"Subcategory {i}.{j}.{k}",
                        countOfNestedWorld=0,
                        parentCategory = subcategory,
                    )
                    
                    # Связываем подкатегорию второго уровня с подкатегорией первого уровня
                

                    # Создаем страницы для каждой конечной подкатегории
                    for page_num in range(1, random.randint(2, 8)):  # 2 страницы для каждой конечной категории
                        Page.objects.create(
                            nameOfPage=f"Page for {sub_subcategory.nameOfCategory} {page_num}",
                            parentCategoryKey=sub_subcategory
                        )

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with sample data'))
