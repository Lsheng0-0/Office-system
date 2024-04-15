import os
import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Institution(models.Model):
    """ 机构表 """
    # Django会自动帮我们生成id，并且是自增的，当然也可以自己创建
    serial = models.IntegerField(verbose_name='序号', help_text='序号')
    # verbose_name注解，可以知道某列代表什么意思
    institution = models.CharField(verbose_name='机构', help_text='机构', max_length=40)
    code = models.UUIDField(verbose_name='唯一标识', help_text='唯一标识', default=uuid.uuid4, editable=False,
                            unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_sign = models.BooleanField(verbose_name='激活', help_text='激活', default=True)

    class Meta:
        verbose_name_plural = verbose_name = '机构'


class Organization(models.Model):
    """ 单位表 """
    # Django会自动帮我们生成id，并且是自增的，当然也可以自己创建
    # id = models.BigAutoField(verbose_name='序号', help_text='序号', primary_key=True)
    # verbose_name注解，可以知道某列代表什么意思
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, limit_choices_to={'is_sign': True})
    code = models.UUIDField(verbose_name='唯一标识', help_text='唯一标识', default=uuid.uuid4, editable=False,
                            unique=True, primary_key=True)
    name = models.CharField(verbose_name='单位名称', help_text='单位名称', max_length=40)
    serial = models.IntegerField(verbose_name='单位序号', help_text='单位序号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_sign = models.BooleanField(verbose_name='激活', help_text='激活', default=True)

    class Meta:
        verbose_name_plural = verbose_name = '单位列表'


class Department(models.Model):
    """ 部门表 """
    unit = models.ForeignKey(Organization, on_delete=models.CASCADE, limit_choices_to={'is_sign': True})
    code = models.UUIDField(verbose_name='唯一标识', help_text='唯一标识', default=uuid.uuid4, editable=False,
                            unique=True, primary_key=True)
    name = models.CharField(verbose_name='部门名称', help_text='部门名称', max_length=40)
    serial = models.IntegerField(verbose_name='部门序号', help_text='部门序号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_sign = models.BooleanField(verbose_name='激活', help_text='激活', default=True)

    class Meta:
        verbose_name_plural = verbose_name = '部门列表'
        unique_together = ('unit', 'code',)  # 使用组合键（Composite Key）

    # def get_display_name(self):
    #     return self.department.split('_')[-1]


class User(AbstractUser):
    """  员工表  """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, limit_choices_to={'is_sign': True}, null=True,
                                   blank=True, verbose_name='部门', help_text='部门')
    name = models.CharField(max_length=15, verbose_name="姓名", help_text="姓名", default=None, null=True, blank=True)
    code = models.UUIDField(verbose_name='唯一标识', help_text='唯一标识', default=uuid.uuid4, editable=False,
                            unique=True)
    gender = models.SmallIntegerField(verbose_name="性别", help_text="性别", choices=((1, "男"), (2, "女")), null=True,
                                      blank=True)
    permissions = models.BooleanField(verbose_name="权限", help_text="权限", blank=True, default=False)
    is_sign = models.BooleanField(verbose_name='激活', help_text='激活', default=True)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'user'
        verbose_name_plural = verbose_name = '用户'


def dynamic_form_path(instance, filename):
    # 根据单位和表单名构建上传路径
    return os.path.join("forms", str(instance.unit.name), filename)


class Forms(models.Model):
    """表单"""
    serial = models.IntegerField(verbose_name='表单序号', help_text='表单序号')
    name = models.CharField(verbose_name="表单名称", help_text="表单名称", max_length=100)
    code = models.UUIDField(verbose_name='唯一标识', help_text='唯一标识', default=uuid.uuid4, editable=False,
                            unique=True, primary_key=True)
    description = models.CharField(verbose_name="表单描述", help_text="表单描述", blank=True, null=True, max_length=200)
    unit = models.ForeignKey(Organization, on_delete=models.CASCADE, limit_choices_to={'is_sign': True})
    url = models.FileField(upload_to=dynamic_form_path, verbose_name='表单路径', blank=False)
    type = models.SmallIntegerField(verbose_name="表单类型", help_text="表单类型", choices=(
        (0, "常设"),
        (1, "临时"),
    ), default=0)
    status = models.SmallIntegerField(verbose_name="表单状态", help_text="表单状态", choices=(
        (0, "未发布"),
        (1, "已发布"),
        (2, "已删除"),
    ), default=0)
    # is_sign = models.BooleanField(verbose_name='激活', help_text='激活', default=True)
    create_user = models.CharField(verbose_name="创建人", help_text="创建人", max_length=40)
    create_time = models.DateTimeField(verbose_name="创建时间", help_text="创建时间", auto_now_add=True)
    delete_time = models.DateTimeField(verbose_name="删除时间", help_text="删除时间", null=True, blank=True)
    delete_user = models.CharField(verbose_name="删除人", help_text="删除人", blank=True, null=True, max_length=40)
    is_sign = models.BooleanField(verbose_name='激活', help_text='激活', default=True)

    class Meta:
        verbose_name_plural = verbose_name = '单位表单'


def dynamic_file_path(instance, filename):
    # 根据单位和表单名构建上传路径
    return os.path.join("files", str(instance.download_unit.name), filename)


class Files(models.Model):
    """文件表"""
    form_name = models.ForeignKey(Forms, on_delete=models.CASCADE, limit_choices_to={'is_sign': True},
                                  verbose_name='表单名', help_text='表单名')
    name = models.CharField(verbose_name='文件名', help_text='文件名', blank=False, max_length=40)
    code = models.UUIDField(verbose_name='唯一标识', help_text='唯一标识', default=uuid.uuid4, editable=False,
                            unique=True)
    url = models.FileField(upload_to=dynamic_file_path, verbose_name='文件路径', blank=False)
    created_at = models.DateTimeField(verbose_name='创建时间', help_text="创建时间", auto_now_add=True)
    is_sign = models.BooleanField(verbose_name='激活', help_text='激活', default=True)
    # 发送
    upload_user = models.CharField(verbose_name='发送人', help_text='发送人', blank=False, max_length=40)
    upload_unit = models.CharField(verbose_name='发送单位', help_text='发送单位', blank=False, max_length=40)
    upload_department = models.CharField(verbose_name='发送部门', help_text='发送部门', null=True, blank=True, max_length=40)
    # 接收
    download_user = models.CharField(verbose_name='接收人', help_text="接收人", null=True, blank=True, max_length=40)
    download_unit = models.ForeignKey(Organization, on_delete=models.CASCADE, limit_choices_to={'is_sign': True},
                                      null=True, blank=True, verbose_name='接收单位', help_text='接收单位')
    status = models.BooleanField(verbose_name='接收状态', help_text='接收状态', default=False)
    download_at = models.DateTimeField(verbose_name='接收时间', help_text='接收时间', null=True, blank=True)

    class Meta:
        verbose_name_plural = verbose_name = '上传文件表'
