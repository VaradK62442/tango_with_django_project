from django import template
from rango.models import Category

register = template.Library()

# refers to template
@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    # returns dict with all category objects
    return {'categories': Category.objects.all(),
            'current_category': current_category}
