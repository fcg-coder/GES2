from django.db import models
from category.models import Category
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os

class Page(models.Model):
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

    nameOfPage = models.CharField('Имя страницы', max_length=50)
    reviewStatus = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, blank=True)
    tagTextBasedMMOs = models.CharField('ТЭГ text_based_MMOs', max_length=20, choices=TEXT_BASED_MMO_CHOICES, blank=True)
    tagGraphicalMMOs = models.CharField('ТЭГ graphical_MMOs', max_length=20, choices=GRAPHICAL_MMO_CHOICES, blank=True)
    parentCoategoryKey = models.ForeignKey(Category, verbose_name='Родительская категория', on_delete=models.CASCADE)
   
    def __str__(self):
        return self.nameOfPage

    class Meta:
        verbose_name = 'Страница виртуального мира'
        verbose_name_plural = 'Страницы виртуальных миров'




class Comment(models.Model):
    commentText = models.TextField('Комментарий')
    publishedDate = models.DateTimeField('Дата публикации')
    ParentPageKey = models.ForeignKey(Page, verbose_name='Страница, на которой оставили комментарий', on_delete=models.CASCADE)
    username = models.CharField('Имя пользователя', max_length=25)


    def __str__(self):
        return self.commentText

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
