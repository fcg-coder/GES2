from django.contrib import admin
from .models import MAP

class MAPAdmin(admin.ModelAdmin):
    list_display = ('nameOfPage', 'parent_page', 'countOfVW', 'id')
    list_filter = ('FlagForInternalRecordings', 'FlagForThePresenceOfAParent')
    search_fields = ('idOfPage',)

admin.site.register(MAP, MAPAdmin)
