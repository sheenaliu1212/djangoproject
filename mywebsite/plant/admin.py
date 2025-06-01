# plant/admin.py
from django.contrib import admin
from .models import Plant, Category, Tag, PlantFavorite

class PlantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Plant, PlantAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PlantFavorite)

class PlantFavoriteAdmin(admin.ModelAdmin):
    list_display = ('plant', 'user', 'created_at')
    search_fields = ('user__username', 'plant__title')
    list_filter = ('created_at',)