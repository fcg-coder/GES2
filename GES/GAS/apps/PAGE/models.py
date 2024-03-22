from django.db import models
from map.models import MAP

class page(models.Model):
    id = models.Index('id', name='Id страницы')
    nameOfPage = models.CharField('Имя страницы', max_length= 50)
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('published', 'Опубликовано'),
    )
    TEXT_BASED_MMO_CHOICES = (
        ('MUD', 'Multi-User Dungeon'),
        ('MUD_OO', 'MUD Object Oriented'),
        ('MUSH', 'Multi-User Shared Hallucination'),
        ('MMORPG', 'MMORPG'),
        ('educational', 'educational'),
        ('social', 'social'),
        ('deadserver', 'deadserver'),
    )
    GRAPHICAL_MMO_CHOICES = (
        ('MMORPG', 'MMORPG'),
        ('MMOCCG', 'MMOCCG'),
        ('sandbox', 'sandbox'),
        ('dance', 'dance'),
        ('kids', 'kids'),
        ('teens', 'teens'),
        ('social', 'social'),
        ('musical', 'musical'),
        ('educational', 'educational'),
        ('deadserver', 'deadserver'),
        ('revived', 'revived by community'),
    )

    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES,  blank=True)
    text_based_MMOs_T = models.CharField('ТЭГ text_based_MMOs', max_length=20, choices=TEXT_BASED_MMO_CHOICES,  blank=True)
    graphical_MMOs_TAG = models.CharField('ТЭГ graphical_MMOs', max_length=20, choices=GRAPHICAL_MMO_CHOICES,  blank=True)
    map = models.ForeignKey(MAP, verbose_name='Родительская категория', on_delete=models.CASCADE)

   
    def __str__(self):
        return self.nameOfPage


    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'