from django.shortcuts import render, redirect
from django.http import HttpResponse
# import datetime
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def set_cookie(request, key, value):
    response = HttpResponse("Cookie 設定成功")
    response.set_cookie(key, value)
    return response

def get_cookie(request, key):
    if key in request.COOKIES:
        value = request.COOKIES.get(key)
        return HttpResponse(f"Cookie {key} 的值是: {value}")
    else:
        return HttpResponse(f"Cookie {key} 不存在")

# 加入有效時間
def set_cookie2(request, key, value):
    response = HttpResponse("Cookie 設定成功，有效時間是1個小時")
    response.set_cookie(key, value, max_age=10)
    return response

def get_allcookies(request):
    # 判斷COOKIES是否有值
    if request.COOKIES != None:
        # 取得COOKIES的值
        strCookies = ""
        for key, value in request.COOKIES.items():
            strCookies += f"{key}: {value}" + "<br>"
        return HttpResponse(strCookies)
    else:
        return HttpResponse("COOKIES 沒有值")

def delete_cookie(request, key):
    if key in request.COOKIES:
        response = HttpResponse("Cookie 刪除成功: " + key)
        response.delete_cookie(key)
        return response
    else:
        return HttpResponse(f"Cookie {key} 不存在")

# session========================================
def set_session(request, key, value):
    response = HttpResponse("Session 設定成功")
    request.session[key] = value
    return response

def get_session(request, key):
    if key in request.session:
        value = request.session.get(key)
        return HttpResponse(f"Session {key} 的值是: {value}")
    else:
        return HttpResponse(f"Session 不存在")
    
def set_session2(request, key=None, value=None):
    response = HttpResponse("Session 設定成功")
    request.session(key, value)
    # 設定session有效時間為30秒
    request.session.set_expiry(30)
    return response

def get_allsessions(request):
    # 判斷COOKIES是否有值
    if request.session != None:
        # 取得COOKIES的值
        strSessions = ""
        for key, value in request.session.items():
            strSessions += f"{key}: {value}" + "<br>"
        return HttpResponse(strSessions)
    else:
        return HttpResponse("session 沒有值")

def delete_session(request, key):
    if key in request.session:
        response = HttpResponse("Session 刪除成功: " + key)
        response.delete_session(key)
        return response
    else:
        return HttpResponse(f"Session 不存在")

def cookie_session(request):
    if "counter" in request.COOKIES:
        # 取得COOKIES的值並轉成整數
        counter = int(request.COOKIES.get("counter"))
        counter += 1
    else:
        counter = 1
    response = HttpResponse("今天訪問次數: " + str(counter))
    #                目前系統時間       +  1天
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = datetime.replace(tomorrow, hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%Y-%m-%d %H:%M:%S GMT")
    # 設定COOKIES的值
    response.set_cookie("counter", counter, expires=expires)
    return response

def vote(request):
    if not "vote" in request.session:
        request.session["vote"] = True
        message = "謝謝您的投票"
    else:
        message = "您已經投過票"
    return HttpResponse(message)

def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        
        # 使用 Django 內建的使用者認證系統驗證
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 使用者驗證成功
            auth_login(request, user)
            request.session["username"] = username
            message = "登入成功！歡迎回來，" + username
            status = "login"
        else:
            # 使用者驗證失敗
            message = "帳號或密碼錯誤，請重新輸入"
            status = "logout"
    else:
        # 檢查是否已經通過Django驗證
        if request.user.is_authenticated:
            # 如果用戶已經通過驗證但還沒有session username
            if "username" not in request.session:
                request.session["username"] = request.user.username
            message = f"您已經成功登入系統，歡迎回來，{request.user.username}"
            status = "login"
        elif "username" in request.session:
            message = "您已經成功登入系統"
            status = "login"
        else:
            message = ""
            status = "logout"
    return render(request, "cookiessessions/login.html", locals())

def logout(request):
    if request.user.is_authenticated or "username" in request.session:
        if "username" in request.session:
            message = request.session["username"] + " 已成功登出系統"
            del request.session["username"]
        else:
            message = request.user.username + " 已成功登出系統"
        auth_logout(request)
    else:
        message = "您尚未登入系統"
    status = "logout"
    return render(request, "cookiessessions/login.html", locals())

def register(request):
    # 預設狀態與訊息
    message = ""
    success = False
    
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        
        # 簡單的表單驗證
        if len(username) < 6:
            message = "帳號長度需大於6個字元"
        elif len(password) < 8:
            message = "密碼長度需大於8個字元"
        elif password != password_confirm:
            message = "兩次密碼輸入不一致"
        elif User.objects.filter(username=username).exists():
            message = "該用戶名已被使用"
        else:
            # 使用Django的User模型創建新用戶
            user = User.objects.create_user(
                username=username,
                password=password
            )
            user.save()
            
            message = "註冊成功！您可以立即登入"
            success = True
            
            # 重定向到登入頁面
            return redirect("/cookiessessions/login/")
    
    return render(request, "cookiessessions/register.html", locals())

# 管理員功能 - 列出所有使用者
def user_list(request):
    # 確認是否為管理員
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/cookiessessions/login/")
    
    # 獲取所有使用者
    users = User.objects.all().order_by('id')
    
    return render(request, "cookiessessions/user_list.html", {'users': users})

# 管理員功能 - 添加使用者
def add_user(request):
    # 確認是否為管理員
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/cookiessessions/login/")
    
    message = ""
    
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        is_staff = request.POST.get("is_staff", "") == "on"
        is_superuser = request.POST.get("is_superuser", "") == "on"
        
        # 表單驗證
        if len(username) < 6:
            message = "帳號長度需大於6個字元"
        elif len(password) < 8:
            message = "密碼長度需大於8個字元"
        elif User.objects.filter(username=username).exists():
            message = "該用戶名已被使用"
        else:
            # 創建新用戶
            user = User.objects.create_user(
                username=username,
                password=password,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            user.save()
            
            message = "新增使用者成功！"
            return redirect("/user_admin/users/")
    
    return render(request, "cookiessessions/add_user.html", locals())

# 管理員功能 - 管理使用者
def manage_users(request):
    # 確認是否為管理員
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/cookiessessions/login/")
    
    message = ""
    
    # 處理刪除用戶請求
    if request.method == "POST" and 'delete_id' in request.POST:
        user_id = request.POST.get("delete_id", "")
        try:
            # 防止刪除admin帳號
            user = User.objects.get(id=user_id)
            if user.username != 'admin':
                user.delete()
                message = "使用者已刪除"
            else:
                message = "不能刪除admin帳號"
        except User.DoesNotExist:
            message = "找不到該使用者"
    
    # 獲取所有使用者
    users = User.objects.all().order_by('id')
    
    return render(request, "cookiessessions/manage_users.html", {'users': users, 'message': message})

# 管理員功能 - 編輯使用者
def edit_user(request, user_id):
    # 確認是否為管理員
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/cookiessessions/login/")
    
    message = ""
    
    try:
        user = User.objects.get(id=user_id)
        
        if request.method == "POST":
            # 不允許更改admin的用戶名
            if user.username != 'admin':
                user.username = request.POST.get("username", user.username)
            
            # 更新密碼（如果提供）
            password = request.POST.get("password", "")
            if password:
                user.set_password(password)
            
            user.is_staff = request.POST.get("is_staff", "") == "on"
            user.is_superuser = request.POST.get("is_superuser", "") == "on"
            user.save()
            
            message = "使用者資料已更新"
            return redirect("/user_admin/users/manage/")
        
    except User.DoesNotExist:
        message = "找不到該使用者"
        return redirect("/user_admin/users/manage/")
    
    return render(request, "cookiessessions/edit_user.html", {'user_obj': user, 'message': message})
