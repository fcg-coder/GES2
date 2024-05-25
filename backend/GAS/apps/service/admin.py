from django.contrib import admin
from .models import feedback
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message')

admin.site.register(feedback, FeedbackAdmin)