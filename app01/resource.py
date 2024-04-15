# -*- coding: UTF-8 -*-
from import_export import resources
from app01.models import *


class InstitutionResource(resources.ModelResource):
    class Meta:
        model = Institution
        skip_unchanged = True
        report_skipped = True
        exclude = 'id'
        fields = ('institution', 'serial', 'created_at', 'state')  # 指定你想导入/导出的字段
        import_id_fields = ['institution']  # 指定主键字段名
        # export_order = ('id', 'email')

class OrganizationAdminResource(resources.ModelResource):
    class Meta:
        model = Organization
        skip_unchanged = True
        report_skipped = True
        exclude = 'id'
        fields = ('unit', 'unit_serial', 'institution', 'created_at', 'state')  # 指定你想导入/导出的字段
        import_id_fields = ['unit']  # 指定主键字段名
        # export_order = ('id', 'email')

# class UserResource(resources.ModelResource):
#     class Meta:
#         model = User
#         skip_unchanged = True
#         report_skipped = True
#         exclude = 'id'
#         import_id_fields = ('username', 'mobile_id', 'depart_id', 'gender', 'password', 'is_active', 'is_staff')
#         # export_order = ('id', 'email')
