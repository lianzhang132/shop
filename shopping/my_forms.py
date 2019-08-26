from django import forms  #自动验证 # forms组件
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from shopping.models import Member
class UserForm(forms.Form):
    wid_01 = widgets.TextInput(attrs={"class": "form-control"})#<input type='text' class="form-control">
    wid_02 = widgets.PasswordInput(attrs={"class": "form-control"})#<input type='password' class="form-control">

    member_name=forms.CharField(max_length=20,min_length=4,label="用户名",widget=wid_01,error_messages={"required":"该字段必填"})
    member_nickname = forms.CharField(max_length=20, min_length=2, label="显示名称", widget=wid_01,
                                  error_messages={"required": "该字段必填"})
    member_pwd=forms.CharField(max_length=16,min_length=6,label="密码",widget=wid_02,validators=[RegexValidator('\d+','只能是数字') ],error_messages={'required': '密码不能为空','min_length': '密码长度不能小于6','max_length': '密码长度不能大于16','invalid': '密码格式错误',})
    r_pwd=forms.CharField(max_length=16,min_length=6,label="确认密码",widget=wid_02,validators=[RegexValidator('\d+','只能是数字') ],error_messages={'required': '密码不能为空','min_length': '密码长度不能小于6','max_length': '密码长度不能大于16','invalid': '密码格式错误',}) #/(?=.*[a-z])(?=.*\d)(?=.*[#@!~%^&*])[a-z\d#@!~%^&*]{8,16}/i
    member_email = forms.EmailField(label="邮箱",widget=wid_01,error_messages={"required":"该字段必填","invalid":"格式不正确"})
    # member_tel = forms.CharField(max_length=11, widget=wid_01,label="电话号码",)

    # 局部钩子
    def clean_member_name(self):
        val = self.cleaned_data.get("member_name")
        res = Member.objects.filter(member_name=val)
        if not res:
            return val
        else:
            raise ValidationError("用户名已存在!")

    # 全局钩子
    def clean(self):
        member_pwd=self.cleaned_data.get("member_pwd")
        r_pwd=self.cleaned_data.get("r_pwd")
        if member_pwd and r_pwd:
            if member_pwd==r_pwd:
                # print(self.cleaned_data)
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致!')
        else:
            return self.cleaned_data



class UserForm1(forms.Form):
    wid_01 = widgets.TextInput(attrs={"class": "form-control"})#<input type='text' class="form-control">
    wid_02 = widgets.PasswordInput(attrs={"class": "form-control"})#<input type='password' class="form-control">
    member_name=forms.CharField(max_length=60,min_length=4,label="用户名",widget=wid_01,error_messages={"required":"该字段必填"})
    member_nickname = forms.CharField(max_length=60, min_length=2, label="显示名称", widget=wid_01,
                                  error_messages={"required": "该字段必填"})
    member_pwd=forms.CharField(max_length=30,min_length=1,label="密码",widget=wid_02,validators=[RegexValidator('\d+','只能是数字') ],error_messages={'required': '密码不能为空','min_length': '密码长度不能小于8','max_length': '密码长度不能大于18','invalid': '密码格式错误',})
    r_pwd=forms.CharField(max_length=30,min_length=1,label="确认密码",widget=wid_02,validators=[RegexValidator('\d+','只能是数字') ],error_messages={'required': '密码不能为空','min_length': '密码长度不能小于8','max_length': '密码长度不能大于18','invalid': '密码格式错误',}) #/(?=.*[a-z])(?=.*\d)(?=.*[#@!~%^&*])[a-z\d#@!~%^&*]{8,16}/i
    member_email = forms.EmailField(label="邮箱",widget=wid_01,error_messages={"required":"该字段必填","invalid":"格式不正确"})
    member_tel = forms.CharField(max_length=11, widget=wid_01,label="电话号码",)

    # 局部钩子
    def clean_member_name(self):
        val = self.cleaned_data.get("member_name")
        res = Member.objects.filter(member_name=val)
        if not res:
            return val
        else:
            raise ValidationError("用户名已存在!")

    # 全局钩子
    def clean(self):
        member_pwd=self.cleaned_data.get("member_pwd")
        r_pwd=self.cleaned_data.get("r_pwd")
        if member_pwd and r_pwd:
            if member_pwd==r_pwd:
                # print(self.cleaned_data)
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致!')
        else:
            return self.cleaned_data
