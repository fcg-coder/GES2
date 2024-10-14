from django.contrib import admin
from .models import Page, Comment

class PageAdmin(admin.ModelAdmin):
    list_display = ('nameOfPage', 'reviewStatus', 'tagTextBasedMMOs', 'tagGraphicalMMOs', 'parentCategoryKey')
    list_filter = ('reviewStatus', 'tagTextBasedMMOs', 'tagGraphicalMMOs', 'parentCategoryKey')
    search_fields = ('nameOfPage', 'tagTextBasedMMOs', 'tagGraphicalMMOs')
    ordering = ('nameOfPage',)

    def save_model(self, request, obj, form, change):
        # Дополнительные действия при сохранении модели (если нужно)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Дополнительные действия при удалении модели (если нужно)
        super().delete_model(request, obj)

# Регистрируем модель Page и её админ-класс
admin.site.register(Page, PageAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'commentText', 'publishedDate', 'ParentPageKey')
    list_filter = ('publishedDate', 'username', 'ParentPageKey')
    search_fields = ('username', 'commentText')
    ordering = ('publishedDate',)

    def save_model(self, request, obj, form, change):
        # Дополнительные действия при сохранении модели (если нужно)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Дополнительные действия при удалении модели (если нужно)
        super().delete_model(request, obj)

# Регистрируем модель Comment и её админ-класс
admin.site.register(Comment, CommentAdmin)
