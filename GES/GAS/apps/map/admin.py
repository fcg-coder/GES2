from django.contrib import admin
from .models import MAP

class MAPAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('nameOfPage', 'idOfPage', 'status')  # Отображаемые поля в списке объектов
    list_filter = ('status',)  # Фильтр по полю статус
    search_fields = ('nameOfPage',)  # Поиск по полю имя страницы
    readonly_fields = ('idOfPage',)  # Поля только для чтения

    fieldsets = (
        ('Основная информация', {
            'fields': ('idOfPage', 'nameOfPage', 'status'),
        }),
    )

    actions = ['publish_selected']  # Действие для публикации выбранных записей

    def publish_selected(self, request, queryset):
        queryset.update(status='published')  # Обновление статуса выбранных записей на "published"

    publish_selected.short_description = 'Опубликовать выбранные записи'  # Название действия в админке
=======
    list_display = ('nameOfPage', 'parent_page', 'countOfVW', 'id')
    list_filter = ('FlagForInternalRecordings', 'FlagForThePresenceOfAParent')
    search_fields = ('idOfPage',)
>>>>>>> master

admin.site.register(MAP, MAPAdmin)
