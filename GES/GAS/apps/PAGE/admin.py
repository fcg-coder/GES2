from django.contrib import admin
from .models import page

class PageAdmin(admin.ModelAdmin):
    list_display = ('nameOfPage', 'status', 'id','map')
    list_filter = ('status',)
    actions = ['publish_pages']

    def publish_pages(self, request, queryset):
        queryset.update(status='published')
    publish_pages.short_description = 'Опубликовать выбранные страницы'

admin.site.register(page, PageAdmin)
