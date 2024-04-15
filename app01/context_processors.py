# myapp/context_processors.py

from django.contrib import admin

def site_header(request):
    # 返回管理员站点标题作为上下文变量
    return {'site_header': admin.site.site_header}

def site_title(request):
    # 返回管理员站点标题作为上下文变量
    return {'site_title': admin.site.site_title}


def index_title(request):
    # 返回管理员站点标题作为上下文变量
    return {'index_title': admin.site.index_title}
