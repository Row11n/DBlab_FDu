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
                return render(request,'Userinfo/register.html',{'form': LoginForm(), 'error_msg': '用户名已存在'})
          
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                return render(request,'Userinfo/register.html',{'form': LoginForm(), 'error_msg': '邮箱已存在'})

            uid_exists = User.objects.filter(uid=uid).exists()
            if uid_exists:
                return render(request,'Userinfo/register.html',{'form': LoginForm(), 'error_msg': '工号已存在'})

           
            User.objects.create_user(username=username,password=password,email=email,uid=uid)
            user = authenticate(request,username=username,password=password)
            login(request,user) # 使用自带的login函数进行登录，会自动添加session信息
            request.session["username"] = username # 自定义session，login函数添加的session不满足时可以增加自定义的session信息。
            return redirect('system:home')
        else:
            return render(request,'Userinfo/register.html',{'form': LoginForm(), 'error_msg': '无效输入，请保持密码一致，检查邮箱格式，且工号只能为10位'})


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
                return redirect('system:home')
            elif user and not user.is_active:
                return render(request,'Userinfo/login.html',{'form': LoginForm(), 'error_msg': '用户未激活'})
            else:
                return render(request,'Userinfo/login.html',{'form': LoginForm(), 'error_msg': '用户名与密码不匹配'})
        else:
            print(form.errors)
            return render(request,'Userinfo/login.html',{'form': LoginForm(), 'error_msg': '无效输入','form.errors':form.errors})