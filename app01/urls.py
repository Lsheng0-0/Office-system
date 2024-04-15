"""
URL configuration for Office system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from . import views
from django.urls import path

urlpatterns = [
    # 前置
    path('login/', views.login_view, name='登录视图'),
    path('logout/', views.logout_view, name='登出视图'),
    path('', views.login_in, name='登录'),

    path('indexview/', views.index_view, name='首页视图'),
    path('index/', views.navigation_index_view, name='首页'),  # 导航插入的index
    path('index/manifestview/', views.manifest_view, name='清单视图'),
    path('index/manifest/', views.navigation_manifest_view, name='清单'),

    path('uploadview/', views.upload_view, name='上传文件'),

    path('password_change/', views.navigation_password_change_view, name='密码更改'),
    path('password_changeview/', views.password_change_view, name='修改密码'),
    path('password_change_success/', views.password_change_success_view, name='修改密码成功'),

    path('submitted/', views.navigation_submitted_view, name='单位发送'),
    path('submittedview/', views.submitted_view, name='单位发送视图'),
    path('submitted_filter/', views.submitted_filter, name='单位发送筛选'),
    path('submitted_export_to_excel/', views.submitted_export_to_excel, name='单位发送导出excel'),

    path('form_management/', views.navigation_form_management_view, name='表单管理视图'),
    path('form_managementview/', views.form_management_view, name='表单管理'),
    path('form_management/add/', views.form_add_view, name='创建表单'),
    path('form_add/', views.form_add, name='添加'),
    path('form_management/edit/', views.form_edit_view, name='编辑表单'),
    path('form_edit/', views.form_edit, name='编辑'),
    path('form_delete/', views.form_delete, name='删除'),
    path('form_management_filter/', views.form_management_filter, name='表单管理筛选'),

    path('receive/', views.navigation_receive_view, name='单位接收'),
    path('receiveview/', views.receive_view, name='单位接收视图'),
    path('receive_sure/', views.receive_sure, name='接收'),
    path('receive_filter/', views.receive_filter, name='单位接收筛选'),
    path('receive_export_to_excel/', views.receive_export_to_excel, name='单位接收导出excel'),


]
