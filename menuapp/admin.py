from django.contrib import admin

from menuapp.models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu_name', 'url', 'order']
    list_filter = ['menu_name']
    search_fields = ['title', 'url']
    ordering = ['order', 'title']
