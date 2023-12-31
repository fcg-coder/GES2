from django.db import models
from map.models import MAP

class page(models.Model):
    id = models.Index('id', name='Id страницы')
    nameOfPage = models.CharField('Имя страницы', max_length= 50)
    idCategory = models.IntegerField('id', name='Id категории')
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('published', 'Опубликовано'),
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES)
    map = models.ForeignKey(MAP, verbose_name='Родительская категория', on_delete=models.CASCADE)

   
    def __str__(self):
        return self.nameOfPage


    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'