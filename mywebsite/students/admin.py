from django.contrib import admin
#    appname.程式            專案名稱
from students.models import Student
# Register your models here.
# 註冊方式一，簡單顯示欄位
# admin.site.register(Student)

# 註冊方式二，透過類別定義管理顯示內容
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'stdName', 'stdSex', 'stdEmail', 'stdPhone']
    # 設定過濾器，在網頁右側可以做資料篩選
    list_filter = ('stdName', 'stdSex')
    # 加入搜尋功能
    search_fields = ('stdName',)
    # 加入排序功能
    ordering = ('id',)
admin.site.register(Student, StudentAdmin)
