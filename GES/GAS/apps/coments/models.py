from django.db import models


#Здесь будут описываться классы(один) коментариев 
class Comment(models.Model):
    comment_text = models.TextField('Коментарий')
    pub_date = models.DateTimeField('Дата публикации')
    document = models.FileField(upload_to='documents/')
    documentName = models.CharField('Имя файла', max_length= 50)
    photo = models.ImageField('Фото')
    documentName = models.CharField('Имя фото', max_length= 50)


    def __str__(self):
        return self.comment_text
    
    
    
    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
