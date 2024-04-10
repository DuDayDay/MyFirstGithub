from django.db import models

# Create your models here.
#创建表结构

class Department(models.Model):
    """部门表"""
    title = models.CharField(max_length=32, verbose_name='部门标题')
    def __str__(self):
        return self.title
class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='账户余额',default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='入职时间')
    # 有约束
    # -to 与哪张表关联
    # -to_field 表中的哪一列
    # 级联删除 on_delete = models,CASCADE
    departe = models.ForeignKey(to='Department',to_field='id',on_delete=models.CASCADE,verbose_name='部门')
    # 置空
    # departe = models.ForeignKey(to='Department',to_field='id',null=True,blank=True,on_delete=models.SET_NULL,verbose_name='置空')
    gender_choice = ((1,'男'),(0,'女'))
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choice,default=1)

class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    # price= models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    price = models.IntegerField(verbose_name='价格')
    level_choice = ((1,'一级'),
                    (2,'二级'),
                    (3,'三级'),
                    (4,'四级'))
    level = models.SmallIntegerField(verbose_name='级别',choices=level_choice,default=1)
    status_choice = ((1,'占号'),(2,'未占号'))
    status = models.SmallIntegerField(verbose_name='状态',choices=status_choice,default=2)

