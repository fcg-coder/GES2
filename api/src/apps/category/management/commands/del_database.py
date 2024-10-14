from django.core.management.base import BaseCommand
from category.models import Category
from page.models import Page

class Command(BaseCommand):
    help = 'Fill the database with sample data'

    def handle(self, *args, **kwargs):
        # Удаляем все записи из базы данных
        Category.objects.all().delete()
        Page.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully delete the database with sample data'))
