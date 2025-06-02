# plant/admin.py
from django.contrib import admin
from .models import Plant, Category, Tag, PlantFavorite

class PlantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'description', 'image', 'video_url')
        }),
        ('分類信息', {
            'fields': ('category', 'tags')
        }),
        ('生長條件', {
            'fields': ('temperature', 'humidity', 'light_requirement'),
            'classes': ('collapse',)
        }),
        ('養護技巧', {
            'fields': ('watering', 'repotting', 'precaution'),
            'classes': ('collapse',)
        }),
        ('用戶相關', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Plant, PlantAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PlantFavorite)

class PlantFavoriteAdmin(admin.ModelAdmin):
    list_display = ('plant', 'user', 'created_at')
    search_fields = ('user__username', 'plant__title')
    list_filter = ('created_at',)