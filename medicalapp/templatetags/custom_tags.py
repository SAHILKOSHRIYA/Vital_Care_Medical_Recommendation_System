from django import template
from medicalapp.models import *
register = template.Library()

@register.filter(name='split_lines')
def split_lines(value):
    return value.split('\n')