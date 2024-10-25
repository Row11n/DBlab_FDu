from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import *
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from django.views.generic import View
from system.models import *
from django.http import Http404

    
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
            user_for_uid = User.objects.order_by('-uid').first()
            _uid = int(user_for_uid.uid) + 10000000001
            __uid = str(_uid)[1:11]
            uid = __uid

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
            return render(request,'Userinfo/register.html',{'form': LoginForm(), 'error_msg': '无效输入，请保持密码一致，检查邮箱格式'})

def register_for_staff(request):
    if(request.user.is_superuser == False):
        raise Http404
    if request.method != 'POST':
        form = RegisterForm()
        context = {'form':form}
        return render(request, 'Userinfo/register_for_staff.html', context)
    else:
        form = RegisterForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            #user_for_uid = User.objects.order_by('-uid').first()
            uid = random.randint(1000000, 9999999)
            # _uid = int(user_for_uid.uid) + 10000000001
            # __uid = str(_uid)[1:11]
            # uid = __uid

            username_exists = User.objects.filter(username=username).exists()
            if username_exists:
                return render(request,'Userinfo/register_for_staff.html',{'form': LoginForm(), 'error_msg': '用户名已存在'})
          
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                return render(request,'Userinfo/register_for_staff.html',{'form': LoginForm(), 'error_msg': '邮箱已存在'})

            uid_exists = User.objects.filter(uid=uid).exists()
            if uid_exists:
                return render(request,'Userinfo/register_for_staff.html',{'form': LoginForm(), 'error_msg': '工号已存在'})

           
            User.objects.create_user_staff(username=username,password=password,email=email,uid=uid)
            request.session["username"] = username # 自定义session，login函数添加的session不满足时可以增加自定义的session信息。
            return render(request,'Userinfo/register_for_staff.html',{'form': LoginForm(), 'msg': '创建成功'})
        else:
            return render(request,'Userinfo/register_for_staff.html',{'form': LoginForm(), 'error_msg': '无效输入，请保持密码一致，检查邮箱格式'})


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

class UserInfoView(View):
    template = 'Userinfo/userinfo.html'
    redirect_authenticated_user = True

    def get(self, request, user_id) :
        user = User.objects.get(id=user_id)
        if(request.user != user):
            raise Http404
        form = UserChangeForm(instance=user)
        next = request.GET.get("next")
        user_list = User.objects.order_by('-is_staff')
        bill_list = Guest_bill.objects.filter(user = user).order_by("status")
        return render(request, self.template, 
            context={'form': form, 'next': next, 'user':user, 'bill_list':bill_list, 'user_list':user_list})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = UserChangeForm(instance=user,data=request.POST,files=request.FILES)
        bill_list = Guest_bill.objects.filter(user = user).order_by("status")
        user_list = User.objects.order_by('-is_staff')
        pay = form.data.get('pay')
        send_back = form.data.get('send_back')
        if form.data.get('bill_id'):
            bill_id = form.data.get('bill_id')
            bill = Guest_bill.objects.get(id = bill_id)
            book = bill.book
        print(pay)
        if pay == "1":
            bill.status = "2"
            bill.save()
            finan = Finance(bill=bill, is_stock=0)
            finan.save()
        if send_back == "1":
            bill.status = "3"
            bill.save()
            book.amount = book.amount + bill.amount
            book.save()
        next = form.data.get('next')
        if next == '':
            next = None
        if form.is_valid():
            form.save()
            return render(request, self.template, 
            context={'form': form, 'next': next,'user':user, 'bill_list':bill_list, 'user_list':user_list})
        else:
            errors = {name:list(form.errors[name]) for name in form.errors}
            return render(request, self.template,
                context={'form': form, 'error_msg': 'Invalid input', 'errors': errors, 'bill_list':bill_list, 'user_list':user_list})


    def get_redirect_url(self, next=None) -> str: 
        if next == 'None' or next is None:
            return '/'
        else:
            return str(next)