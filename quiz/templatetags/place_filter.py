
from django import template

register = template.Library()

@register.filter(name='index_counter')
def counter(page_number):
    return int((page_number-1)*15)

@register.filter(name='divide')
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None
