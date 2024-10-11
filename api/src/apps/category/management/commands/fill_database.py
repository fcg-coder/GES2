from django.core.management.base import BaseCommand
from category.models import Category
from page.models import Page


class Command(BaseCommand):
    help = 'Fill the database with sample data'

    def handle(self, *args, **kwargs):
        # Удаляем все записи из базы данных
        Category.objects.all().delete()
        Page.objects.all().delete()

        # Создаем 2 родительские категории
        parent_categories = []
        for i in range(1, 3):  # 2 родительские категории
            parent_category = Category.objects.create(
                nameOfCategory=f"Parent Category {i}",
                countOfNestedWorld=0,
                

            )
            parent_categories.append(parent_category)

            # Создаем несколько подкатегорий для каждой родительской категории
            for j in range(1, 4):  # 3 подкатегории
                subcategory = Category.objects.create(
                    nameOfCategory=f"Subcategory {i}.{j}",
                    countOfNestedWorld=0,
                  
                )
                
                # Связываем подкатегорию с родительской категорией
                parent_category.link_child(subcategory)

                # Создаем подкатегории второго уровня
                for k in range(1, 3):  # 2 подкатегории второго уровня
                    sub_subcategory = Category.objects.create(
                        nameOfCategory=f"Subcategory {i}.{j}.{k}",
                        countOfNestedWorld=0,
                       
                    )
                    
                    # Связываем подкатегорию второго уровня с подкатегорией первого уровня
                    subcategory.link_child(sub_subcategory)

                    # Создаем страницы для каждой конечной подкатегории
                    for page_num in range(1, 3):  # 2 страницы для каждой конечной категории
                        Page.objects.create(
                            nameOfPage=f"Page for {sub_subcategory.nameOfCategory} {page_num}",
                            parentCategoryKey=sub_subcategory
                        )

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with sample data'))
