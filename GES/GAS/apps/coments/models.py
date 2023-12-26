from django.db import models
import os

#Здесь будут описываться классы(один) коментариев 
class Comment(models.Model):
    comment_text = models.TextField('Коментарий')
    pub_date = models.DateTimeField('Дата публикации')
    document = models.FileField(upload_to='documents/')
    documentName = models.CharField('Имя файла', max_length= 50)
    idOfPage = models.IntegerField('Id страницы')
    username = models.CharField('Имя пользователя', max_length= 25)
    adminNameComment = models.TextField('Имя объекта')
    
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
