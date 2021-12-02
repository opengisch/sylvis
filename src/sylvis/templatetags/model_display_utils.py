from django import template

register = template.Library()


@register.filter
def get_class_name(value):
    return value.__class__.__name__


@register.filter
def get_model_verbose_name(value):
    return value._meta.verbose_name
