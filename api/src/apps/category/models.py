from django.db import models  # Импортируем базовый класс models для создания моделей базы данных
from django.db.models.signals import post_save  # Импортируем сигнал post_save для обработки событий после сохранения модели
from django.dispatch import receiver  # Импортируем декоратор receiver для связывания сигналов с обработчиками
from django.db.models import Sum
from django.apps import apps


class Category(models.Model):  # Определяем модель Category, которая будет представлять категорию в базе данных
    id = models.AutoField(primary_key=True)  # Поле id, автоматически увеличиваемое и являющееся первичным ключом
    nameOfCategory = models.CharField('Имя категории', max_length=50)  # Поле для хранения имени категории, ограниченное 50 символами
    countOfNestedWorld = models.IntegerField('Количество миров', default=0)  # Поле для хранения количества подкатегорий, по умолчанию 0

    parentCategory = models.ForeignKey(
            'self', 
            verbose_name='Родительская категория', 
            null=True, 
            blank=True, 
            on_delete=models.CASCADE, 
            related_name='subcategories'  # Добавлено для получения подкатегорий
        )
    childCategoies = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_pages')  # Поле для хранения многих внутренних страниц (дочерних категорий)

    flagForInternalRecordings = models.BooleanField('Есть подкатегории', default=False)  # Флаг, указывающий, есть ли подкатегории
    flagForThePresenceOfAParent = models.BooleanField('Есть родительская категория', default=False)  # Флаг, указывающий, есть ли родительская категория

    def __str__(self):  # Метод для строкового представления объекта категории
        return self.nameOfCategory  # Возвращает имя категории

    class Meta:  # Класс Meta для метаданных модели
        verbose_name = 'Категория'  # Человекочитаемое имя модели в единственном числе
        verbose_name_plural = 'Категории'  # Человекочитаемое имя модели во множественном числе


    def save(self, *args, update_parent=True, **kwargs):  # Переопределяем метод save с аргументом update_parent по умолчанию
        if update_parent:
            self.flagForThePresenceOfAParent = self.parentCategory is not None  # Устанавливаем флаг наличия родительской категории

           
        if not getattr(self, '_skip_signal', False):
            self._skip_signal = True
            super().save(*args, **kwargs)
            self._skip_signal = False
        else:
            super().save(*args, **kwargs)

        if self.parentCategory is not None:
            self.parentCategory.childCategoies.add(self)  # Добавляем дочернюю категорию в поле childCategoies родительской категории
            self.parentCategory.flagForInternalRecordings = True
            self.parentCategory.save(update_parent=False)  # Передаем False, чтобы предотвратить рекурсию




    # Запускается при сохранении объекта Page 
    # Рекурсивно обновляет всем родительским категориям количество миров
    def update_count_of_virtual_worlds(self):
    
        if not self.flagForInternalRecordings:
            Page = apps.get_model('page', 'Page') 
            self.countOfNestedWorld = Page.objects.filter(parentCategoryKey=self).count()
        else:
            # Если категория имеет подкатегории, считаем количество миров для подкатегорий
            self.countOfNestedWorld = self.subcategories.aggregate(Sum('countOfNestedWorld'))['countOfNestedWorld__sum'] or 0

        # Сохраняем изменения
        self.save(update_fields=['countOfNestedWorld'])

        # Если есть родительская категория, обновляем ее рекурсивно
        if self.parentCategory:
            self.parentCategory.update_count_of_virtual_worlds()

   
