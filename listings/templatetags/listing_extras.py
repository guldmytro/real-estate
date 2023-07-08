from django import template
import re
from django.utils.translation import gettext_lazy as _

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