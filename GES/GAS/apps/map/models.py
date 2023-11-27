from django.db import models

class MAP(models.Model):
    id = models.Index('id', name='Id страницы')

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = 'Id'
        verbose_name_plural = 'Id'