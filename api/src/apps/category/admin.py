from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nameOfCategory', 'countOfNestedWorld', 'parentPage', 'flagForInternalRecordings', 'flagForThePresenceOfAParent')
    list_filter = ('flagForInternalRecordings', 'flagForThePresenceOfAParent', 'parentPage')  # Фильтры для боковой панели
    search_fields = ('nameOfCategory',)  # Поля для поиска
    ordering = ('nameOfCategory',)  # Упорядочивание по имени категории

    def save_model(self, request, obj, form, change):
        # Дополнительные действия при сохранении модели (если нужно)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Дополнительные действия при удалении модели (если нужно)
        super().delete_model(request, obj)

# Регистрируем модель и её админ-класс
admin.site.register(Category, CategoryAdmin)
