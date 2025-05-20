from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from news.models import NewsUnit, Category
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

@login_required
def add_news(request):
    if not request.user.is_staff:
        return redirect('/news/')
    
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category', "")
        author = request.user.username
        image = request.FILES.get('image', None)
        link = request.POST.get('link', "").strip()
        is_show = request.POST.get('is_show', "") == 'on'

        if title and content and category_id:
            category = get_object_or_404(Category, id=category_id)
            news = NewsUnit(
                title=title, 
                content=content, 
                category=category, 
                author=author, 
                image=image, 
                link=link, 
                is_show=is_show)
            # 建立新聞公告
            news.save()
            return redirect('/news/')
        else:
            return render(request, 'news/add_news.html', locals())
        
@login_required
def delete_news(request, news_id):
    if not request.user.is_staff:
        return redirect('/news/')
    
    newsItem = get_object_or_404(NewsUnit, id=news_id)

    if request.method == 'POST':
        newsItem.delete()
        return redirect('/news/')

    return render(request, 'news/delete_news.html', locals())

def edit_news(request, news_id):
    if not request.user.is_staff:
        return redirect('/news/')
    
    newsItem = get_object_or_404(NewsUnit, id=news_id)

    if request.method == 'POST':
        newsItem.delete()
        return redirect('/news/')

    return render(request, 'news/edit_news.html', locals())