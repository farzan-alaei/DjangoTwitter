# templatetags/form_filters.py
from django import template

register = template.Library()


@register.filter(name="add_classes")
def add_classes(value, arg):
    return value.as_widget(attrs={"class": arg})
