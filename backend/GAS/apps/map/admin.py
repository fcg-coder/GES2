from django.contrib import admin
from .models import MAP

class MAPAdmin(admin.ModelAdmin):
    list_display = ('nameOfPage', 'parent_page', 'countOfVW', 'id')
    list_filter = ('FlagForInternalRecordings', 'FlagForThePresenceOfAParent')
    search_fields = ('nameOfPage',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Если у объекта есть родитель, вызываем функцию связывания
        if obj.parent_page:
            obj.parent_page.link_child(obj)

admin.site.register(MAP, MAPAdmin)
