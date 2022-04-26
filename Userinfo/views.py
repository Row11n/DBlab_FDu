from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import *
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
    
User = get_user_model() # 获取User模型

def register(request):
    if request.method != 'POST':
        form = RegisterForm()
        context = {'form':form}
        return render(request, 'Userinfo/register.html', context)
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            uid = form.cleaned_data["uid"]
            username_exists = User.objects.filter(username=username).exists()
            if username_exists:
             return JsonResponse({"code":400,"message":"验证失败","data":{"username":"您输入的用户名已存在!","password1":"","password2":"","email":"","uid":""}})
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                return JsonResponse({"code": 400, "message":"验证失败","data":{"username": "","password1":"","password2":"", "email": "您输入的邮箱已存在！","uid":""}})
            uid_exists = User.objects.filter(uid=uid).exists()
            if email_exists:
                return JsonResponse({"code": 400, "message":"验证失败","data":{"username": "","password1":"","password2":"", "email": "","uid":"工号重复"}})
            User.objects.create_user(username=username,password=password,email=email,uid=uid)
            return JsonResponse({"code": 200,"message":"验证通过", "data":{"username": "","password1":"","password2":"", "email": "","uid":""}})
        else:
            return JsonResponse({"code":400,"message":"验证失败","data":{"username":form.errors.get("username"),"password1":form.errors.get("password1"),"password2":form.errors.get("password2"),"email":form.errors.get("email")}})



def loginView(request):
    if request.method != 'POST':
        form = LoginForm()
        context = {'form':form}
        return render(request, 'Userinfo/login.html', context)
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            #remember = int(request.POST.get("remember"))
            user = authenticate(request,username=username,password=password) # 使用authenticate进行登录验证，验证成功会返回一个user对象，失败则返回None
            # 使用authenticate验证时如果is_active为False也会返回None，导致无法判断激活状态，
            # 此时可以在seetings中配置：
            # AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']
            if user and user.is_active: # 如果验证成功且用户已激活执行下面代码
                login(request,user) # 使用自带的login函数进行登录，会自动添加session信息
                request.session["username"] = username # 自定义session，login函数添加的session不满足时可以增加自定义的session信息。
                #if remember:
                #    request.session.set_expiry(None) # 设置session过期时间，None表示使用系统默认的过期时间 
                #else:
                #    request.session.set_expiry(0) # 0代表关闭浏览器session失效
                return redirect('system:home')
            elif user and not user.is_active:
               return JsonResponse({"code": 400, "message": "用户未激活", "data": {"error": "该用户还没有激活，请<a href='#'>激活</a>"}})
            else:
                return JsonResponse({"code": 400, "message": "验证失败", "data": {"error": "用户名或密码错误"}})
        else:
            return JsonResponse({"code":400,"message":"用户名或密码格式错误","data":{"error":"用户名或密码错误"}})