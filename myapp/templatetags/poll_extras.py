from django import template
from myapp.models import *
register = template.Library()

@register.simple_tag(name="getproducts")
def get_categories():
    return Products.objects.all()

@register.inclusion_tag('wablon.html')
def show_categories():
    admin = Admins.objects.all()
    return {'admin': admin}

