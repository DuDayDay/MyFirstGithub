from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.models import PrettyNum


# Create your views here.
def depart_list(request):
    """ 部门列表 """

    # 数据库中获取所有部门
    # [ {} {} {} ...{}]
    queryset = models.Department.objects.all()
    return render(request,'depart_list.html' ,{'queryset':queryset})
def depart_add(request):
    """ 添加部门 """
    if request.method == 'GET':
        return render(request,'depart_add.html')
    # 获取数据
    title = request.POST.get('title' )
    # print(title)
    models.Department.objects.create(title=title)
    # 重新回到部门列表
    return redirect("/depart/list")
def depart_delete(request):
    # 获取id
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    # 返回部门列表
    return redirect("/depart/list")
def depart_edit(request,nid):
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request,'depart_edit.html',{'row_object':row_object})
    """修改部门"""
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list")
def user_list(request):
    querset = models.UserInfo.objects.all()
    return render(request,'user_list.html',{'querset':querset})
def user_add(request):
    if request.method == 'GET':
        context = {
            'gender_choice': models.UserInfo.gender_choice,
            'depart_list': models.Department.objects.all()
        }
        return render(request,'user_add.html',context)
    # 获取数据

    name = request.POST.get('name')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    count = request.POST.get('count')
    # createtime = request.POST.get('createtime')
    depart_id = request.POST.get('depart')
    password = request.POST.get('password')

    models.UserInfo.objects.create(name=name,age=age,gender=gender,account=count, departe_id=depart_id,password=password)
    return redirect("/user/list")
class UserForm(forms.ModelForm):

    name = forms.CharField(max_length=4,label='用户名')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'age', 'gender', 'account','departe', 'password']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name,field in self.fields.items():
                field.widget.attrs = {'class':"form-control"}
def user_model_form_add(request):
    if request.method == 'GET':
        """添加用户 (ModelForm)"""
        form = UserForm()
        return render(request,'user_model_form_add.html',{"form":form})
    # 用户POST提交数据，数据校验
    form = UserForm(data=request.POST)
    if form.is_valid():
        # 数据合法则保存到数据库
        form.save()
        return redirect("/user/list")
    else:
        # 校验失败
        return render(request,'user_model_form_add.html',{"form":form})

def user_edit(request,nid):
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        """编辑用户"""
        # 根据id去数据库获取数据
        # row_obj = models.UserInfo.objects.filter(id=nid).first()
        # 将数据库中获取的信息传递到页面
        form = UserForm(instance=row_obj)
        return render(request,'user_edit.html', {'form':form})

    # row_obj = models.UserInfo.objects.filter(id=nid).first()
    form = UserForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        # 添加额外的数据
        # form.instance.字段名 = value
        form.save()
        return redirect("/user/list")
    return render(request, 'user_model_form_add.html', {"form": form})

def user_delete(request,nid):
    row_obj = models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list")

def pretty_list(request):
    qureyset= models.PrettyNum.objects.all().order_by('-level')
    return render(request,'pretty_list.html', {'qureyset':qureyset})
class PrettyNumViewSet(forms.ModelForm):
    # model = forms.CharField(
    #     label='手机号码',
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误'),]
    # )
    class Meta():
        model = models.PrettyNum
        fields = "__all__" # 所有字段
        # exclude = ['level'] # 除了哪个字段
# 添加格式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': "form-control"}
# 提交字段的校验
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if len(txt_mobile) != 11:
            # 验证通过
            raise ValidationError("格式错误")
        elif exists:
            raise ValidationError("手机号已经存在")
        # 验证通过
        return txt_mobile
def pretty_add(request):
    if request.method == 'GIT':
        """ 添加靓号"""
        form = PrettyNumViewSet()
        return render(request,'pretty_add.html', {"form":form})
    form = PrettyNumViewSet(data=request.POST)
    if form.is_valid():
        # 数据合法则保存到数据库
        form.save()
        return redirect("/pretty/list")
    else:
        # 校验失败
        return render(request,'pretty_add.html',{"form":form})


class PrettyListEdit(forms.ModelForm):
    mobile = forms.CharField(disabled=True, label='手机号码')
    class Meta:
        model = models.PrettyNum
        fields = ['mobile','price','level','status']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': "form-control"}

def pretty_edit(request,nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        """编辑靓号"""
        # 根据id去数据库获取数据
        # row_obj = models.UserInfo.objects.filter(id=nid).first()
        # 将数据库中获取的信息传递到页面
        form = PrettyListEdit(instance=row_obj)
        return render(request,'pretty_edit.html', {'form':form})

    form = PrettyListEdit(data=request.POST, instance=row_obj)
    if form.is_valid():
        # 添加额外的数据
        # form.instance.字段名 = value
        form.save()
        return redirect("/pretty/list")
    return render(request, 'pretty_edit.html', {"form": form})