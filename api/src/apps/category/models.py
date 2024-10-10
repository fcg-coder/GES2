from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    nameOfCatergory = models.CharField('Имя категории', max_length=50)
    countOfNestedWorld = models.IntegerField('Количество миров', default=0)

    parentPage = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_pages')
    internalPages = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_pages')

    flagForInternalRecordings = models.BooleanField('Есть подкатегории', default=False)
    flagForThePresenceOfAParent = models.BooleanField('Есть родительская категория', default=False)

    def __str__(self):
        return self.nameOfCatergory

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_parent_categories(self):
        # Получаем родительские категории, в которые входит данная категория
        return Category.objects.filter(internalPages=self)

    def save(self, *args, **kwargs):
        # Определяем значение флагов перед сохранением
        self.FlagForThePresenceOfAParent = self.parentPage is not None

        # Пропускаем сигнал при сохранении модели, чтобы избежать рекурсии
        if not getattr(self, '_skip_signal', False):
            self._skip_signal = True
            super().save(*args, **kwargs)
            self._skip_signal = False
        else:
            super().save(*args, **kwargs)

    def link_child(self, child):
        """ Связывает дочернюю категорию с текущей категорией """
        child.parentPage = self
        child.save()
        
        # Добавляем дочернюю категорию в список внутренних страниц родителя
        self.internalPages.add(child)
        self.FlagForInternalRecordings = True
        self.save()

@receiver(post_save, sender=Category)
def update_internal_recordings(sender, instance, **kwargs):
    # Обновляем флаг наличия внутренних записей после сохранения объекта
    if not instance._skip_signal:
        instance.FlagForInternalRecordings = instance.internalPages.exists()
        instance._skip_signal = True
        instance.save()
        instance._skip_signal = False
