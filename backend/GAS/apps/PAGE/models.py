from django.db import models
from map.models import MAP
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db import models
import os


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
        verbose_name = 'Страница виртуального мира'
        verbose_name_plural = 'Страницы виртувльных миров'








#Здесь будут описываться классы(один) коментариев 
class Comment(models.Model):
    comment_text = models.TextField('Коментарий')
    pub_date = models.DateTimeField('Дата публикации')
    document = models.FileField(upload_to='documents/')
    documentName = models.CharField('Имя файла', max_length= 50)
    cat = models.ForeignKey(page, verbose_name='Страница на которой оставили комментарий', on_delete=models.CASCADE)
    username = models.CharField('Имя пользователя', max_length= 25)
    adminNameComment = models.TextField('Имя комментария')
    
    def is_image_file(self):
        # Получаем расширение файла
        _, file_extension = os.path.splitext(self.document.path)

        # Список расширений файлов изображений
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

        # Проверяем, является ли расширение файла изображением
        if file_extension.lower() in image_extensions:
            return True
        else:
            return False

    def __str__(self):
        return self.adminNameComment
    
   
    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'


    
@receiver(pre_delete, sender=Comment)
def delete_comment_document(sender, instance, **kwargs):
    # Удаление документа при удалении комментария
    default_storage.delete(instance.document.path)
