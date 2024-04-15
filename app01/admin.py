from import_export.admin import ImportExportModelAdmin
from app01.models import User, Organization, Forms, Institution, Department, Files
from django import forms
from django.contrib import admin

from app01.resource import InstitutionResource, OrganizationAdminResource

admin.site.site_header = '濂溪区统一表单系统'  # 设置header
admin.site.site_title = '濂溪区统一表单系统'  # 设置title
admin.site.index_title = '濂溪区统一表单系统'


@admin.register(Institution)
class InstitutionAdmin(ImportExportModelAdmin):
    resource_class = InstitutionResource
    list_display = ('institution', 'serial', 'code', 'created_at', 'is_sign')  # 展示
    list_editable = ('serial', 'is_sign')  # 负责修改
    search_fields = ['institution', ]  # 搜索
    list_filter = ('created_at', 'is_sign')  # 筛选
    list_per_page = 12  # 分页
    ordering = ['-serial', 'serial']  # 优先级排序


@admin.register(Organization)
class OrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationAdminResource
    list_display = ('name', 'serial', 'get_institution_name', 'code', 'created_at', 'is_sign')  # 展示
    list_editable = ('serial', 'is_sign',)  # 负责修改
    search_fields = ['name', 'institution__institution', ]
    list_per_page = 12  # 分页
    ordering = ['-serial', 'serial']  # 优先级排序

    def get_institution_name(self, obj):
        return obj.institution.institution if obj.institution else ''

    get_institution_name.short_description = '机构'


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'serial', 'get_unit_name', 'code', 'created_at', 'is_sign')  # 展示
    list_editable = ('serial', 'is_sign')  # 负责修改
    search_fields = ['name', 'get_unit_name']
    list_filter = ('serial', 'is_sign')
    list_per_page = 12  # 分页
    ordering = ['-serial', 'serial']  # 优先级排序

    def get_unit_name(self, obj):
        return obj.unit.name if obj.unit else ''

    get_unit_name.short_description = '单位'


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('username', 'name', 'gender', 'get_department_name', 'code', 'permissions', 'is_sign', 'is_active',
                    'is_staff', 'last_login')  # 展示
    list_editable = ('gender', 'permissions', 'is_sign', 'is_active', 'is_staff')  # 负责修改
    search_fields = ['username', 'name', ]
    list_filter = ('permissions',)
    list_per_page = 12  # 分页
    ordering = ['id', '-id']  # 优先级排序

    def get_department_name(self, obj):
        return obj.department.unit.name if obj.department else ''

    get_department_name.short_description = '单位'


@admin.register(Forms)
class FormsAdmin(ImportExportModelAdmin):
    list_display = ('name', 'serial', 'description', 'get_unit_name', 'url', 'type', 'status', 'code',
                    'create_user', 'create_time','delete_time','is_sign')  # 展示
    list_editable = ('serial', 'type', 'status','is_sign')  # 负责修改
    search_fields = ['name', 'get_unit_name', 'create_user', 'delete_user']
    list_filter = ('type', 'status')
    list_per_page = 12  # 分页
    ordering = ['serial', '-serial']  # 优先级排序

    def get_unit_name(self, obj):
        return obj.unit.name if obj.unit else ''

    get_unit_name.short_description = '单位'


@admin.register(Files)
class FilesAdmin(ImportExportModelAdmin):
    list_display = (
        'name', 'get_form_name', 'code', 'url', 'created_at', 'is_sign', 'upload_user', 'upload_unit',
        'get_download_unit_name', 'status')  # 展示
    list_editable = ('is_sign', 'status',)  # 负责修改
    search_fields = ['name', 'upload_unit', 'get_download_unit_name']
    list_filter = ('status',)
    list_per_page = 12  # 分页
    ordering = ['id', '-id']  # 优先级排序

    def get_form_name(self, obj):
        return obj.form_name.name if obj.form_name else ''

    get_form_name.short_description = '表单名'

    def get_download_unit_name(self, obj):
        return obj.download_unit.name if obj.download_unit else ''

    get_download_unit_name.short_description = '接收单位'
