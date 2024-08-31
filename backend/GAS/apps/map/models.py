from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class MAP(models.Model):
    id = models.AutoField(primary_key=True)
    FlagForInternalRecordings = models.BooleanField('Есть подкатегории', default=False)
    nameOfPage = models.CharField('Имя категории', max_length=50)
    FlagForThePresenceOfAParent = models.BooleanField('Есть родительская категория', default=False)
    internal_pages = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_pages')
    countOfVW = models.IntegerField('Количество миров', default=0)
    parent_page = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_pages')

    def __str__(self):
        return self.nameOfPage

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_parent_categories(self):
        # Получаем родительские категории, в которые входит данная категория
        return MAP.objects.filter(internal_pages=self)

    def save(self, *args, **kwargs):
        # Определяем значение флагов перед сохранением
        self.FlagForThePresenceOfAParent = self.parent_page is not None

        # Пропускаем сигнал при сохранении модели, чтобы избежать рекурсии
        if not getattr(self, '_skip_signal', False):
            self._skip_signal = True
            super().save(*args, **kwargs)
            self._skip_signal = False
        else:
            super().save(*args, **kwargs)

    def link_child(self, child):
        """ Связывает дочернюю категорию с текущей категорией """
        child.parent_page = self
        child.save()
        
        # Добавляем дочернюю категорию в список внутренних страниц родителя
        self.internal_pages.add(child)
        self.FlagForInternalRecordings = True
        self.save()

@receiver(post_save, sender=MAP)
def update_internal_recordings(sender, instance, **kwargs):
    # Обновляем флаг наличия внутренних записей после сохранения объекта
    if not instance._skip_signal:
        instance.FlagForInternalRecordings = instance.internal_pages.exists()
        instance._skip_signal = True
        instance.save()
        instance._skip_signal = False

def countOfVirW(VWS):
    Pages = MAP.objects.all()
    for Page in Pages:
        Page.countOfVW = 0
        Page.save()

    startPages = MAP.objects.filter(FlagForInternalRecordings=False)
    for startPage in startPages:
        for VW in VWS:
            if VW.map == startPage:
                startPage.countOfVW += 1
        startPage.save()
    
        page = startPage
        while page.FlagForThePresenceOfAParent:
            parentPages = page.get_parent_categories()

            for parentPage in parentPages:
                parentPage.countOfVW += startPage.countOfVW
                parentPage.save()

            # Используйте родителя для следующей итерации
            if parentPages.exists():
                page = parentPages.first()
            else:
                break
