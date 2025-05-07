from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from news.models import NewsUnit
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    # 抓資料表所有資料的方法
    # 資料表.objects.all()[.order_by(欄位名稱)]
    # NewsUnit.objects.all().order_by('id')
    newsData = NewsUnit.objects.all().order_by('id')
    # 分頁控制，每頁顯示 10 筆資料。資料是上一行程式由 stdData 取得
    paginator = Paginator(newsData, 10)
    #                           ?page=  後面的值
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "news/index.html", locals())

def detail(request, detail_id=None):
    newsItem = get_object_or_404(NewsUnit, id=detail_id)
    newsItem.click_count += 1
    newsItem.save()
    return render(request, 'news/detail.html', locals())
