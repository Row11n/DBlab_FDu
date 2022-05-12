from django.forms import Form
from django.forms import fields
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import(
    ReadOnlyPasswordHashField, AuthenticationForm
)
from .models import *

class RegisterForm(Form):
    username = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            "required":"用户名不可以为空！",
            "min_length":"用户名不能低于3位！",
            "max_length":"用户名不能超过18位！"
        }
    )
    password1 = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            "required":"密码不可以空",
            "min_length": "密码不能低于3位！",
            "max_length": "密码不能超过18位！"
        }
    )
    password2 = fields.CharField(required=False)
    email = fields.EmailField(
        required=True,
        error_messages={
            "required":"邮箱不可以为空！"
        },
    )

    def clean_password2(self):
        if not self.errors.get("password1"):
            if self.cleaned_data["password2"] != self.cleaned_data["password1"]:
                raise ValidationError("您输入的密码不一致，请重新输入！")
            return self.cleaned_data



class LoginForm(Form):
    username = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            "required":"用户名不可以为空！",
            "min_length":"用户名不能低于3位！",
            "max_length":"用户名不能超过18位！"
        }
    )
    password = fields.CharField(
        required=True,
        widget=forms.PasswordInput,
        error_messages={
            "required":"密码不可以空",
        }
    )


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('avatar','uid', 'realname', 'gender','phone',
                    'email', 'birthday')