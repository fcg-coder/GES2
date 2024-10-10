from django.db import models  # Импортируем базовый класс models для создания моделей базы данных
from django.db.models.signals import post_save  # Импортируем сигнал post_save для обработки событий после сохранения модели
from django.dispatch import receiver  # Импортируем декоратор receiver для связывания сигналов с обработчиками

class Category(models.Model):  # Определяем модель Category, которая будет представлять категорию в базе данных
    id = models.AutoField(primary_key=True)  # Поле id, автоматически увеличиваемое и являющееся первичным ключом
    nameOfCatergory = models.CharField('Имя категории', max_length=50)  # Поле для хранения имени категории, ограниченное 50 символами
    countOfNestedWorld = models.IntegerField('Количество миров', default=0)  # Поле для хранения количества подкатегорий, по умолчанию 0

    parentPage = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_pages')  # Поле для ссылки на родительскую категорию (если есть)
    internalPages = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_pages')  # Поле для хранения многих внутренних страниц (дочерних категорий)

    flagForInternalRecordings = models.BooleanField('Есть подкатегории', default=False)  # Флаг, указывающий, есть ли подкатегории
    flagForThePresenceOfAParent = models.BooleanField('Есть родительская категория', default=False)  # Флаг, указывающий, есть ли родительская категория

    def __str__(self):  # Метод для строкового представления объекта категории
        return self.nameOfCatergory  # Возвращает имя категории

    class Meta:  # Класс Meta для метаданных модели
        verbose_name = 'Категория'  # Человекочитаемое имя модели в единственном числе
        verbose_name_plural = 'Категории'  # Человекочитаемое имя модели во множественном числе

    def get_parent_categories(self):  # Метод для получения родительских категорий
        # Получаем родительские категории, в которые входит данная категория
        return Category.objects.filter(internalPages=self)  # Возвращает все категории, которые имеют данную категорию как внутреннюю

    def save(self, *args, **kwargs):  # Переопределяем метод save для добавления логики при сохранении
        # Исправляем флаг на правильный атрибут
        self.flagForThePresenceOfAParent = self.parentPage is not None  # Устанавливаем флаг наличия родительской категории

        if not getattr(self, '_skip_signal', False):  # Проверяем, установлен ли флаг для пропуска сигнала
            self._skip_signal = True  # Устанавливаем флаг, чтобы избежать повторного вызова сигналов
            super().save(*args, **kwargs)  # Вызываем метод save родительского класса
            self._skip_signal = False  # Сбрасываем флаг
        else:
            super().save(*args, **kwargs)  # Если флаг установлен, просто сохраняем без сигналов

    def link_child(self, child):  # Метод для связывания дочерней категории с родительской
        child.parentPage = self  # Устанавливаем текущую категорию как родительскую для дочерней
        child.save()  # Сохраняем дочернюю категорию

        # Добавляем дочернюю категорию в список внутренних страниц родителя
        self.internalPages.add(child)  # Добавляем дочернюю категорию в поле internalPages родительской категории

        # Обновляем правильный флаг
        self.flagForInternalRecordings = bool(self.internalPages.count())  # Устанавливаем флаг наличия подкатегорий на основе количества внутренних страниц
        self.save()  # Сохраняем изменения в родительской категории
