from django.contrib import admin
# 同路徑下的models.py檔案
from .models import NewsUnit, Category, NewsReply

# Register your models here.
admin.site.register(Category)
# admin.site.register(NewsUnit)

class NewsUnitAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date',)
    list_display = ('title', 'category', 'author', 'pub_date')
    search_fields = ('title', 'content')
    list_filter = ('category', 'pub_date')
    fieldsets = (
        ('分類', {'fields': ['category']}),
        ('基本信息',{'fields': ('title', 'content', 'author', 'is_show', 'click_count', 'link')}),
        ('日期', {'fields': ['pub_date']}),
        ('圖片', {'fields':['image']}),
    )

class NewsReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'user', 'created_at')
    search_fields = ('user__username', 'content')
    # 設定過濾欄位，tuple資料一定要有逗號
    list_filter = ['created_at']
    # 設定日期階層，利用日期階層進行篩選
    date_hierarchy = 'created_at'
    # 設置欄位的排序方式，-
    ordering = ('-created_at',)

admin.site.register(NewsUnit, NewsUnitAdmin)
admin.site.register(NewsReply, NewsReplyAdmin)