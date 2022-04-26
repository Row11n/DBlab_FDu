from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def _create_user(self,username,password,email,uid,**kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        if not email:
            raise ValueError("请传入邮箱地址！")
        if not uid:
            raise ValueError("工号不可为空")
        user = self.model(username=username,email=email,uid=uid,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_user(self,username,password,email,uid,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username,password,email,uid,**kwargs)
    def create_superuser(self,username,password,email,uid,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username,password,email,uid,**kwargs)

class User(AbstractBaseUser,PermissionsMixin): # 继承AbstractBaseUser，PermissionsMixin
    GENDER_TYPE = (
        ("1","男"),
        ("2","女")
    )
    uid = models.CharField(max_length=10,primary_key=True,verbose_name="工号")
    username = models.CharField(max_length=15,verbose_name="用户名",unique=True)
    nickname = models.CharField(max_length=13,verbose_name="昵称",null=True,blank=True)
    age = models.IntegerField(verbose_name="年龄",null=True,blank=True)
    gender = models.CharField(max_length=2,choices=GENDER_TYPE,verbose_name="性别",null=True,blank=True)
    phone = models.CharField(max_length=11,null=True,blank=True,verbose_name="手机号码")
    email = models.EmailField(verbose_name="邮箱")
    picture = models.ImageField(upload_to="Store/user_picture",verbose_name="用户头像",null=True,blank=True)
    is_active = models.BooleanField(default=True,verbose_name="激活状态")
    is_staff = models.BooleanField(default=True,verbose_name="是否是员工")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'uid']
    EMAIL_FIELD = 'email'
    objects = UserManager()
    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
