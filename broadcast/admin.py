from django.contrib import admin
from django.utils.html import format_html
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'display_image')
    search_fields = ('title',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'