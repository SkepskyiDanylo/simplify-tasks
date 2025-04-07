from django import template

register = template.Library()


@register.filter
def format_phone_number(value):
    return f'+{value[:1]} {value[1:4]} {value[4:6]} {value[6:]}'
