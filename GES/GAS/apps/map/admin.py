from django.contrib import admin
from .models import MAP

class MAPAdmin(admin.ModelAdmin):
    list_display = ('nameOfPage', 'id', 'status', 'FlagForInternalRecordings','FlagForThePresenceOfAParent')
    list_filter = ('status', 'FlagForInternalRecordings')
    search_fields = ('nameOfPage',)
    filter_horizontal = ('internal_pages',)

    fieldsets = (
        ('Основная информация', {
            'fields': ( 'nameOfPage', 'status', 'FlagForInternalRecordings','FlagForThePresenceOfAParent', 'internal_pages'),
        }),
    )

    actions = ['publish_selected']  # Действие для публикации выбранных записей

    def publish_selected(self, request, queryset):
        queryset.update(status='published')  # Обновление статуса выбранных записей на "published"

    publish_selected.short_description = 'Опубликовать выбранные записи'  # Название действия в админке

admin.site.register(MAP, MAPAdmin)
