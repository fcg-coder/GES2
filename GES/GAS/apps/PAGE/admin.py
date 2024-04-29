from django.contrib import admin
from .models import page

class PageAdmin(admin.ModelAdmin):
    list_display = ('nameOfPage', 'id','map', 'text_based_MMOs_T', 'graphical_MMOs_TAG' , 'status')
    list_filter = ('status' , 'text_based_MMOs_T', 'graphical_MMOs_TAG' )
    actions = ['publish_pages']

    def publish_pages(self, request, queryset):
        queryset.update(status='published')
    publish_pages.short_description = 'Опубликовать выбранные страницы'

admin.site.register(page, PageAdmin)
