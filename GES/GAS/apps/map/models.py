from django.db import models


class MAP(models.Model):
    id = models.Index('id', name='Id страницы')
    idOfPage = id
    page_id = id
    FlagForInternalRecordings= models.IntegerField('Флаг на наличие внутренних записей', default=0)

    FlagForThePresenceOfAParent = models.IntegerField('Флаг на наличие родителя', default=0)
    internal_pages = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_pages')
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('published', 'Опубликовано'),
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES)
    nameOfPage = models.CharField('Имя страницы', max_length= 50)
    def __str__(self):
        return self.nameOfPage

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'