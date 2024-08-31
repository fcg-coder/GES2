from django.contrib import admin
from .models import Comment  # Импорт модели Comment
from .models import page

class PageAdmin(admin.ModelAdmin):
    list_display = ('nameOfPage', 'id','map', 'text_based_MMOs_T', 'graphical_MMOs_TAG' , 'status')
    list_filter = ('status' , 'text_based_MMOs_T', 'graphical_MMOs_TAG' )
    actions = ['publish_pages']

    def publish_pages(self, request, queryset):
        queryset.update(status='published')
    publish_pages.short_description = 'Опубликовать выбранные страницы'

admin.site.register(page, PageAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'adminNameComment', 'pub_date', 'is_image_file')  # Поля, которые будут отображаться в списке
    list_filter = ('pub_date', 'username')  # Фильтры для боковой панели
    search_fields = ('username', 'adminNameComment', 'comment_text')  # Поля для поиска
    readonly_fields = ('document',)  # Поля, доступные только для чтения (для предотвращения изменения документа через админку)

    def is_image_file(self, obj):
        return obj.is_image_file()
    is_image_file.boolean = True
    is_image_file.short_description = 'Image File'

    def save_model(self, request, obj, form, change):
        # Дополнительные действия при сохранении модели (если нужно)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Дополнительные действия при удалении модели (если нужно)
        super().delete_model(request, obj)
        # Удаление документа после удаления записи
       

# Регистрируем модель и её админ-класс
admin.site.register(Comment, CommentAdmin)
