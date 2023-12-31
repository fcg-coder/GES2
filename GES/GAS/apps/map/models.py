from django.db import models


class MAP(models.Model):
    id = models.Index('id', name='Id страницы')
    idOfPage = id
    page_id = id
    FlagForInternalRecordings= models.IntegerField('Флаг на наличие подкатегорий')
    nameOfPage = models.CharField('Имя категории', max_length= 50)
    FlagForThePresenceOfAParent = models.IntegerField('Флаг на наличие родительской категории')
    internal_pages = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_pages')

    def __str__(self):
        return self.nameOfPage
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'