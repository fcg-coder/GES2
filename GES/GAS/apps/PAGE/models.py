from django.db import models


class page(models.Model):
    id = models.Index('id', name='Id страницы')


    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'