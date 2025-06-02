from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

# 定義分類名稱欄位
class Category(models.Model):
    title = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.title
    
# 定義標籤名稱欄位
class Tag(models.Model):
    title = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.title

# 定義商品資料欄位
class Plant(models.Model):
    title = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    slug = models.SlugField(blank=True, default="")
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='plants/', null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)
    temperature = models.CharField(max_length=255, default="", blank=True, help_text="溫度需求")
    humidity = models.CharField(max_length=255, default="", blank=True, help_text="濕度需求")
    light_requirement = models.CharField(max_length=255, default="", blank=True, help_text="光照需求")
    watering = models.CharField(max_length=255, default="", blank=True, help_text="澆水頻率")
    repotting = models.CharField(max_length=255, default="", blank=True, help_text="換盆建議")
    precaution = models.CharField(max_length=255, default="", blank=True, help_text="注意事項")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    favorite_users = models.ManyToManyField(User, related_name='favorite_plants', through='PlantFavorite', through_fields=('plant', 'user'))

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("detail", args=[str(self.slug)])

# 定義收藏關聯模型
class PlantFavorite(models.Model):
    plant = models.ForeignKey("Plant", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} favorites {self.plant.title}"