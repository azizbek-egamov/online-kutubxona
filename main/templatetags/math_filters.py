from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='division')
def division(value, arg):
    if arg != 0:
        return value / arg
    return None
