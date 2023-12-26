from django.contrib import admin
from .models import Comment
import os

class CommentAdmin(admin.ModelAdmin):
    list_display = ('adminNameComment', 'comment_text', 'pub_date', 'is_image_file')  # Отображаемые поля в списке объектов
    list_filter = ('pub_date',)  # Фильтр по полю дата публикации
    search_fields = ('adminNameComment', 'username')  # Поиск по полям имя объекта и имя пользователя
    readonly_fields = ('is_image_file',)  # Поле только для чтения

    fieldsets = (
        ('Основная информация', {
            'fields': ('adminNameComment', 'comment_text', 'pub_date', 'document', 'documentName', 'idOfPage', 'username'),
        }),
    )

    def is_image_file(self, obj):
        if obj.document and obj.document.path:
            _, file_extension = os.path.splitext(obj.document.path)
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            return file_extension.lower() in image_extensions
        return False

    is_image_file.boolean = True
    is_image_file.short_description = 'Файл изображения?'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Проверяем, является ли объект существующим (редактирование)
            return self.readonly_fields + ('document',)  # Добавляем поле 'document' в поле только для чтения
        return self.readonly_fields

admin.site.register(Comment, CommentAdmin)
