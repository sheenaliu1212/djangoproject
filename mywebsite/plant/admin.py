# plant/admin.py
from django.contrib import admin
from .models import Plant, Category, Tag

class PlantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Plant, PlantAdmin)
admin.site.register(Category)
admin.site.register(Tag)