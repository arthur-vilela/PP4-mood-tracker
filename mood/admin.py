from django.contrib import admin
from .models import Mood

# Register your models here.

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood_type', 'note', 'action', 'created_at', 'updated_at')
    list_filter = ('mood_type', 'date', 'created_at')
    search_fields = ('user__username', 'mood_type', 'note', 'action')
