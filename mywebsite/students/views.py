from django.shortcuts import render, redirect
from students.models import Student
from students.forms import PostForm
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    # 抓資料表所有資料的方法
    # 資料表.objects.all()[.order_by(欄位名稱)]
    # Student.objects.all().order_by('id')
    stdData = Student.objects.all().order_by('id')
    # 分頁控制，每頁顯示 10 筆資料。資料是上一行程式由 stdData 取得
    paginator = Paginator(stdData, 10)
    #                           ?page=  後面的值
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "students/index.html", locals())

def stdSearch(request):
    # 抓資料表一筆資料的方法
    # 資料表.objects.get(查詢條件)
    # Student.objects.get(stdName="陳曉雯")
    # 避免查不到資料出現錯誤，用try...except包起來
    try:     # 要完成的任務
        result = Student.objects.get(stdName="陳曉X")
    except:  # 錯誤或例外發生時要執行的程式
        errormessage = "(讀取錯誤!)"
    return render(request, "students/stdSearch.html", locals())

def stdFormModel(request):
    # 建立表單驗證物件進階用法
    if request.method == 'POST':
        postform = PostForm(request.POST)
        if postform.is_valid():
            # 處理表單數據
            # 變數接資料    前端網頁傳過來的資料
            stdNamePost = request.POST["stdName"]
            stdSexPost = request.POST["stdSex"]
            stdBirthdayPost = request.POST["stdBirthday"]
            stdEmailPost = request.POST["stdEmail"]
            stdPhonePost = request.POST["stdPhone"]
            stdAddrPost = request.POST["stdAddress"]
            # 將資料新增至資料表
            # 資料表欄位名稱=變數名稱(從 request.POST 取得資料)
            unit = Student.objects.create(
                stdName=stdNamePost,
                stdSex=stdSexPost,
                stdBirthday=stdBirthdayPost,
                stdEmail=stdEmailPost,
                stdPhone=stdPhonePost,
                stdAddress=stdAddrPost
            )
            # 將內容寫入資料庫
            unit.save()
            return redirect('/students/index/')
    else:
        postform = PostForm()
    
    return render(request, 'students/stdFormModel.html', locals())

def stdForm(request):
    if request.method == "POST":
        #             request.GET()
        # 變數接資料    前端網頁傳過來的資料
        stdNamePost = request.POST["abcTest"]
        stdSexPost = request.POST["stdSex"]
        stdBirthdayPost = request.POST["stdBirthday"]
        stdEmailPost = request.POST["stdEmail"]
        stdPhonePost = request.POST["stdPhone"]
        stdAddrPost = request.POST["stdAddress"]
        # 將資料新增至資料表
        # 資料表欄位名稱=變數名稱(從 request.POST 取得資料)
        unit = Student.objects.create(
            stdName=stdNamePost,
            stdSex=stdSexPost,
            stdBirthday=stdBirthdayPost,
            stdEmail=stdEmailPost,
            stdPhone=stdPhonePost,
            stdAddress=stdAddrPost
        )
        # 將內容寫入資料庫
        unit.save()

        return redirect("/students/index/")
    else:
        message = "請輸入資料(資料未作驗證)"
    return render(request, "students/stdForm.html", locals())
  
def delete(request, id=None): #刪除資料
    if id != None:
        if request.method == "POST": #如果是以 POST 方式才處理
            id = request.POST['stdId'] #取得表單輸入的編號
        try:
            unit = Student.objects.get(id=id)
            unit.delete()
            return redirect('/students/index/')
        except:
            message = "讀取錯誤!"
    return render(request, "students/delete.html", locals())

def edit(request, id=None, mode=None):
    if mode == "edit":    # edit.html 的 form 表單的 action 是 /edit/{{unit.id}}/edit
        unit = Student.objects.get(id=id)
        unit.stdName = request.GET["stdName"]
        unit.stdSex = request.GET["stdSex"]
        unit.stdBirthday = request.GET["stdBirthday"]
        unit.stdEmail = request.GET["stdEmail"]
        unit.stdPhone = request.GET["stdPhone"]
        unit.stdAddress = request.GET["stdAddress"]
        unit.save()
        message = "資料修改成功!"
        return redirect("/students/index/")
    else:    # 從網址列傳過來的
        try:
            unit = Student.objects.get(id=id)
            #              datetime 轉成 str
            strdate = str(unit.stdBirthday)
            strdate2 = strdate.replace("年", "-")
            strdate2 = strdate.replace("月", "-")
            strdate2 = strdate.replace("日", "")
            unit.stdBirthday = strdate2
        except:
            message = "這個id不存在，讀取錯誤!"
    return render(request, "students/edit.html", locals())


def edit2(request, id=None, mode=None):
    if mode == "save":    # edit2.html 的 form 表單的 action 是 /edit/{{unit.id}}/save
        unit = Student.objects.get(id=id)
        unit.stdName = request.POST["stdName"]
        unit.stdSex = request.POST["stdSex"]
        unit.stdBirthday = request.POST["stdBirthday"]
        unit.stdEmail = request.POST["stdEmail"]
        unit.stdPhone = request.POST["stdPhone"]
        unit.stdAddress = request.POST["stdAddress"]
        unit.save()
        message = "資料修改成功!"
        return redirect("/students/index/")
    elif mode == "load":    # 從網址列傳過來的
        unit = Student.objects.get(id=id)
        #              datetime 轉成 str
        strdate = str(unit.stdBirthday)
        strdate2 = strdate.replace("年", "-")
        strdate2 = strdate.replace("月", "-")
        strdate2 = strdate.replace("日", "")
        unit.stdBirthday = strdate2
        return render(request, "students/edit2.html", locals())