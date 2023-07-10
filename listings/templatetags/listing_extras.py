from django import template
import re
from django.utils.translation import gettext_lazy as _
from django.template import TemplateSyntaxError
from django.utils.translation import get_language

register = template.Library()


@register.filter
def wrap_words_in_span(value):
    words = re.findall(r'\w+', value)
    wrapped_words = [f'<span>{word}</span>' for word in words]
    return ' '.join(wrapped_words)


@register.simple_tag(takes_context=True)
def url_with_query_params(context, page_number):
    request = context['request']
    query_params = request.GET.copy()
    query_params['page'] = page_number

    url = request.path + '?' + query_params.urlencode()

    return url

@register.filter
def clean_phone(value):
    return re.sub(r'\D+', '', str(value))


@register.filter
def pluralize_uk(value, forms):
    forms = forms.split(',')
    if len(forms) != 3:
        return value

    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    if value % 10 == 1 and value % 100 != 11:
        return f'{value} {forms[0]}'
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return f'{value} {forms[1]}'
    else:
        return f'{value} {forms[2]}'
    

@register.simple_tag
def break_loop():
    raise StopIteration
    