from django.db import models

# 定義分類名稱欄位
class Category(models.Model):
    title = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.title
    
# Create your models here.
class NewsUnit(models.Model):
    # 設定新聞訊息類別
    # 外鍵關連到Category模型，使用PROTECT保護策略防止刪除已被引用的分類，允許為空
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT) 
    # 發佈新聞訊息的人
    author = models.CharField(max_length=20, null=False)
    # 新聞訊息的標題
    title = models.CharField(max_length=100, null=False)
    # 新聞訊息的內容，使用TextField，可以儲存較長的文字
    content = models.TextField(null=False)
    # 新聞訊息的發佈時間
    pub_date = models.DateTimeField(auto_now_add=True)
    # 是否允許顯示
    is_show  = models.BooleanField(default=False)
    # 點擊次數
    click_count = models.IntegerField(default=0)
    # 新聞訊息的圖片
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    # 新聞訊息的連結
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title