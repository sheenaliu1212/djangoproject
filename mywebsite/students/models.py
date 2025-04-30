from django.db import models

# Create your models here.
class Student(models.Model):
    # 定義資料表欄位
    stdName = models.CharField(max_length=20, null=False)
    stdSex = models.CharField(max_length=2, default='M', null=False)
    stdBirthday = models.DateField(null=False)
    stdEmail = models.EmailField(max_length=100, blank=True, null=True)
    stdPhone = models.CharField(max_length=50, blank=True, null=True)
    stdAddress = models.CharField(max_length=255, blank=True, null=True)

    # 定義物件在管理介面顯示的方式，只顯示學生姓名
    def __str__(self):
        return self.stdName
        
