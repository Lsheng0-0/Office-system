from django import template

register = template.Library()

def translation(key):
    items = {
        'Index': '首页',
        'Manifest': '表单',
        'Submitted': '单位发送',
        'Receive': '单位接收',
        'management': '表单管理',
    }
    return items.get(key, key)

@register.simple_tag
def breadcrumb_trail(trail):
    items = trail.split('/')
    breadcrumb = ''
    breadcrumb_list = []
    for item in items:
        if item != '':
            breadcrumb += f'/{item}'
            entag = item.capitalize().split('_')[-1]
            breadcrumb_list.append((translation(entag), breadcrumb))
    return breadcrumb_list
