# custom_filters.py

from django import template

register = template.Library()


@register.filter
def split_url(url):
    return url.name.split('/')
