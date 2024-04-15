import io
import os
import re
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from openpyxl import Workbook

from app01.models import User, Organization, Institution, Forms, Files, Department


# 导航
def _navigation(request, jump):
    user = request.user  # 获取当前登录用户对象
    permission = User.objects.get(username=request.user).permissions
    unit = User.objects.get(username=user).department.unit.name
    department = User.objects.get(username=user).department.name
    name = User.objects.get(username=user).name
    context = {
        "permission": permission,
        "user": name,
        "unit": unit,
        "department": department,
        "jump": jump,
    }
    return context


# 分页
def _paginator(request, datas, num):
    paginator = Paginator(datas, num)
    page_number = request.GET.get("page")  # 获取当前页码
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # 当页面为空时，将用户重定向到最后一页
        page_obj = paginator.get_page(paginator.num_pages)
    return page_obj


def login_in(request):
    return redirect("/login/")


# 登录策略
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/index/")  # 替换为所需的重定向
        else:
            return HttpResponseRedirect("/login/?error=" + str(1))  # 替换为所需的重定向
    else:
        return render(request, "login/login.html")  # 替换为您的登录表单模板


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)  # 注销当前用户的登录状态
    return redirect("/login/")  # 重定向到登录页面


@login_required(login_url="/login/")
def index_view(request):
    institutions = Institution.objects.all().order_by("serial")
    organizations = Organization.objects.all().order_by("serial")
    context = {
        "institutions": institutions,
        "organizations": organizations,
    }
    return render(request, "index/index.html", context)


@login_required(login_url="/login/")
def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponseRedirect("/password_change_success/")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "registration/password_change_form.html", {"form": form})


@login_required(login_url="/login/")
def password_change_success_view(request):
    return render(request, "registration/password_change_done.html")


@login_required(login_url="/login/")
def receive_view(request):
    permission = User.objects.get(username=request.user).permissions
    unitcode = User.objects.get(username=request.user).department.unit.code
    unit_obj = Organization.objects.get(code=unitcode)
    files_obj = Files.objects.filter(download_unit=unit_obj, is_sign=True).order_by(
        "-created_at"
    )
    page_obj = _paginator(request, files_obj, 13)
    context = {
        "permission": permission,
        "receive_list": page_obj,
        "page_obj": page_obj,
        "current_page": request.GET.get("page"),
    }
    # print(context)
    return render(request, "receive/receive.html", context)


def receive_sure(request):
    filecode = request.GET.get("filecode")
    page = request.GET.get("page")
    file = get_object_or_404(Files, code=filecode)
    file.status = True
    file.download_at = timezone.now()
    file.save()
    return HttpResponseRedirect("/receiveview/?page=" + page)


@login_required(login_url="/login/")
def form_management_view(request):
    permission = User.objects.get(username=request.user).permissions
    unit_code = User.objects.get(username=request.user).department.unit.code
    forms_list = Forms.objects.filter(unit=unit_code).order_by("serial")
    # print(forms)
    page_obj = _paginator(request, forms_list, 13)
    context = {
        "permission": permission,
        "forms_list": page_obj,
        "page_obj": page_obj,
        "current_page": request.GET.get("page"),
    }
    # print(context)
    return render(request, "forms/form_management.html", context)


@login_required(login_url="/login/")
def form_add_view(request):
    permission = User.objects.get(username=request.user).permissions
    unit_code = User.objects.get(username=request.user).department.unit.code
    forms_list = Forms.objects.filter(unit=unit_code).order_by("serial")
    # print(forms)
    page_obj = _paginator(request, forms_list, 13)
    page = request.GET.get("page")
    context = {
        "permission": permission,
        "forms_list": page_obj,
        "page_obj": page_obj,
        "current_page": request.GET.get("page"),
    }
    return render(request, "forms/add form.html", context=context)


@login_required(login_url="/login/")
def form_add(request):
    if request.method == "POST":
        user = request.user  # 获取当前登录用户对象
        serial = request.POST.get("sequence")
        name = request.POST.get("formName")
        if Forms.objects.filter(name=name).exists():
            # 如果存在重复值，处理重复值的情况，比如返回错误信息或者执行其他操作
            message = "表单名已存在，请检查输入"
            response = HttpResponse(
                '<script>alert("{}"); window.history.back();</script>'.format(message)
            )
            return response
        else:
            description = request.POST.get("description")
            unit_obj = User.objects.get(username=user).department.unit
            file = request.FILES.get("file_upload")
            status = request.POST.get("status")
            create_user = User.objects.get(username=user).name
            add_form = Forms(
                serial=serial,
                name=name,
                description=description,
                unit=unit_obj,
                url=file,
                status=status,
                create_user=create_user,
            )
            add_form.save()
            page = request.GET.get("page")
            return HttpResponseRedirect("/form_managementview/?page=" + page)


@login_required(login_url="/login/")
def form_edit_view(request):
    formcode = request.GET.get("formcode")
    page = request.GET.get("page")
    unit_code = User.objects.get(username=request.user).department.unit.code
    forms_obj = Forms.objects.filter(unit=unit_code).order_by("serial")
    page = _paginator(request, forms_obj, 13)
    context = {
        "forms_list": page,
        "form_code": formcode,
        "page_obj": page,
        "current_page": request.GET.get("page"),
    }
    return render(request, "forms/edit form.html", context)


@login_required(login_url="/login/")
def form_edit(request):
    formcode = request.GET.get("formcode")
    # 获取要修改的书籍对象
    form = get_object_or_404(Forms, pk=formcode)
    if request.method == "POST":
        # 获取POST请求中提交的数据
        sequence = request.POST.get("sequence")
        formName = request.POST.get("formName")
        if Forms.objects.filter(name=formName).exists():
            if form.name != formName:
                # 如果存在重复值，处理重复值的情况，比如返回错误信息或者执行其他操作
                message = "表单名已存在，请检查输入"
                response = HttpResponse(
                    '<script>alert("{}"); window.history.back();</script>'.format(
                        message
                    )
                )
                return response

        description = request.POST.get("description")
        fileUpload = request.FILES.get("file_upload")
        status = request.POST.get("status")
        create_user = User.objects.get(username=request.user).name
        create_time = timezone.now()
        # 更新书籍对象的值
        form.serial = sequence
        form.name = formName
        form.description = description
        if fileUpload:
            # 删除旧文件
            if form.url and os.path.exists(form.url.path):
                os.remove(form.url.path)
            form.url = fileUpload
        form.status = status
        form.create_user = create_user
        form.create_time = create_time
        form.save()
        page = request.GET.get("page")
        return HttpResponseRedirect("/form_managementview/?page=" + page)


@login_required(login_url="/login/")
def form_delete(request):
    formcode = request.GET.get("formcode")
    form_obj = Forms.objects.get(code=formcode)
    form_obj.name = form_obj.name + "|" + str(formcode) + "(已删除)"
    form_obj.is_sign = False
    form_obj.status = 2
    form_obj.delete_time = timezone.now()
    form_obj.save()
    page = request.GET.get("page")
    return HttpResponseRedirect("/form_managementview/?page=" + page)


@login_required(login_url="/login/")
def submitted_view(request):
    permission = User.objects.get(username=request.user).permissions
    unit = User.objects.get(username=request.user).department.unit.name
    files_obj = Files.objects.filter(upload_unit=unit, is_sign=True).order_by(
        "-created_at"
    )
    page = _paginator(request, files_obj, 13)
    context = {
        "permission": permission,
        "submit_list": page,
        "page_obj": page,
    }
    # print(context)
    return render(request, "submit/submitted.html", context)


@login_required(login_url="/login/")
def submitted_export_to_excel(request):
    submit_list = request.GET.get("submitted")
    # 提取括号中的序号
    numbers = re.findall(r"\((\d+)\)", submit_list)
    # 使用 sorted() 函数按从小到大排序
    sorted_numbers = sorted(numbers, key=int)
    n = 0
    data = []
    for number in sorted_numbers:
        file = Files.objects.get(id=int(number))
        if file.status:
            status = "已接收"
        else:
            status = "未接收"
        line = [
            "{}".format(n + 1),
            file.upload_user,
            file.upload_unit,
            file.form_name.name,
            file.name,
            file.created_at,
            file.download_unit.name,
            status,
        ]
        n += 1
        data.append(line)
    # 创建一个新的工作簿
    wb = Workbook()
    ws = wb.active
    # 添加表头
    ws.append(
        [
            "序号",
            "发送人",
            "发送单位",
            "表单名称",
            "文件名",
            "发送时间",
            "接收单位",
            "接收状态",
        ]
    )
    # 获取要导出的数据列表（假设 data 是您要导出的数据列表）
    # 将数据添加到工作表
    for row in data:
        ws.append(row)
    # 将工作簿保存到 BytesIO 对象中
    buffer = io.BytesIO()
    wb.save(buffer)
    # 将 BytesIO 对象的内容作为响应发送给客户端
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=export.xlsx"
    return response


@login_required(login_url="/login/")
def receive_export_to_excel(request):
    receive_list = request.GET.get("receive")
    # 提取括号中的序号
    numbers = re.findall(r"\((\d+)\)", receive_list)
    # 使用 sorted() 函数按从小到大排序
    sorted_numbers = sorted(numbers, key=int)
    n = 0
    data = []
    for number in sorted_numbers:
        file = Files.objects.get(id=int(number))
        if file.download_at is None:
            download_at = "待接收"
        else:
            download_at = file.created_at
        if file.status:
            status = "已接收"
        else:
            status = "未接收"
        line = [
            "{}".format(n + 1),
            file.form_name.name,
            file.name,
            file.upload_unit,
            file.upload_user,
            file.created_at,
            download_at,
            status,
        ]
        n += 1
        data.append(line)
    # 创建一个新的工作簿
    wb = Workbook()
    ws = wb.active
    # 添加表头
    ws.append(
        [
            "序号",
            "表单名称",
            "文件名",
            "发送单位",
            "发送人",
            "发送时间",
            "接收时间",
            "接收状态",
        ]
    )
    # 获取要导出的数据列表（假设 data 是您要导出的数据列表）
    # 将数据添加到工作表
    for row in data:
        ws.append(row)
    # 将工作簿保存到 BytesIO 对象中
    buffer = io.BytesIO()
    wb.save(buffer)
    # 将 BytesIO 对象的内容作为响应发送给客户端
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=export.xlsx"
    return response


@login_required(login_url="/login/")
def manifest_view(request):
    unit_name = request.GET.get("unitname")
    user = request.user  # 获取当前登录用户对象
    users = User.objects.get(username=user)
    org_uuid = Organization.objects.get(name=unit_name).code
    forms = Forms.objects.filter(unit=org_uuid).order_by("serial")
    # print(users.permissions)
    context = {
        "forms": forms,
        "users": users,
        "organization_name": unit_name,
    }
    # print(context)
    return render(request, "unit/manifest.html", context)


@login_required(login_url="/login/")
def upload_view(request):
    user = request.user  # 获取当前登录用户对象
    if request.method == "POST" and request.FILES.get("file"):
        # 处理文件上传逻辑
        users = User.objects.get(username=user)
        form_code = request.POST.get("form_code")
        form_instance = Forms.objects.get(code=form_code)
        # created_at =
        is_sign = True
        upload_user = users.name
        upload_unit = Department.objects.get(code=users.department.code).unit.name
        upload_department = users.department.name
        download_user = ""
        download_unit = request.POST.get("form_unit_name")
        download_unit_instance = Organization.objects.get(name=download_unit)
        # download_department =
        name = ""
        x = 1
        for file in request.FILES.getlist("file"):
            user_file = Files(
                form_name=form_instance,
                name=file.name,
                is_sign=is_sign,
                upload_user=upload_user,
                url=file,
                upload_unit=upload_unit,
                upload_department=upload_department,
                download_user=download_user,
                download_unit=download_unit_instance,
            )  # 创建UserFile对象，关联用户和文件信息
            user_file.save()  # 保存到数据库
            name += str(x) + "." + file.name + "|"
            x += 1
        # 返回一个带有JavaScript弹窗的响应
        response = HttpResponse(
            '<script>alert("文件:{} 上传成功！"); window.history.back();</script>'.format(
                name
            )
        )
        return response
    else:
        response = HttpResponse(
            '<script>alert("请选择文件上传！"); window.history.back();</script>'
        )
        return response


def filter_objects(request, template_name, model, context_key, search_filters):
    query = request.GET.get("q")
    if query is not None:
        user_department_unit = User.objects.get(username=request.user).department.unit
        filter_condition = {
            "submit_list": {"upload_unit": user_department_unit.name},
            "forms_list": {"unit": user_department_unit},
            "receive_list": {"download_unit": user_department_unit},
        }.get(context_key, {})

        filtered_objects = model.objects.filter(
            is_sign=True,
            **filter_condition,
            **next(
                filter(
                    lambda f: model.objects.filter(
                        is_sign=True, **filter_condition, **f
                    ).exists(),
                    search_filters,
                ),
                {},
            ),
        )
        paginator = Paginator(filtered_objects, 13)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "permission": User.objects.get(username=request.user).permissions,
            context_key: page_obj,
            "page_obj": page_obj,
            "query": query,
            "search_filters": request.GET.urlencode(),
        }
    else:
        context = {}

    return render(request, template_name, context)


@login_required(login_url="/login/")
def submitted_filter(request):
    search_filters = [
        {"name__icontains": request.GET.get("q")},
        {"form_name__name__icontains": request.GET.get("q")},
        {"download_unit__name__icontains": request.GET.get("q")},
    ]
    return filter_objects(
        request, "submit/submitted.html", Files, "submit_list", search_filters
    )


@login_required(login_url="/login/")
def form_management_filter(request):
    search_filters = [
        {"name__icontains": request.GET.get("q")},
        {"create_user__icontains": request.GET.get("q")},
    ]
    return filter_objects(
        request, "forms/form_management.html", Forms, "forms_list", search_filters
    )


@login_required(login_url="/login/")
def receive_filter(request):
    search_filters = [
        {"form_name__name__icontains": request.GET.get("q")},
        {"upload_unit__icontains": request.GET.get("q")},
    ]
    return filter_objects(
        request, "receive/receive.html", Files, "receive_list", search_filters
    )


@login_required(login_url="/login/")
def navigation_manifest_view(request):
    unit_name = request.GET.get("unitname")
    context = _navigation(request, "/index/manifestview/?unitname={}".format(unit_name))
    return render(request, "navigation/navigation.html", context)


@login_required(login_url="/login/")
def navigation_index_view(request):
    try:
        var = Department.objects.get(
            code=User.objects.get(username=request.user).department_id
        ).unit_id
        context = _navigation(request, "/indexview/")
        return render(request, "navigation/navigation.html", context)
    except:
        return redirect("/admin/")


@login_required(login_url="/login/")
def navigation_password_change_view(request):
    context = _navigation(request, "/password_change_success/")
    return render(request, "navigation/navigation.html", context)


@login_required(login_url="/login/")
def navigation_submitted_view(request):
    context = _navigation(request, "/submittedview/")
    return render(request, "navigation/navigation.html", context)


@login_required(login_url="/login/")
def navigation_form_management_view(request):
    context = _navigation(request, "/form_managementview/")
    return render(request, "navigation/navigation.html", context)


@login_required(login_url="/login/")
def navigation_receive_view(request):
    context = _navigation(request, "/receiveview/")
    return render(request, "navigation/navigation.html", context)
