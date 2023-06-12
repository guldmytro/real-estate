from django import template
import re

register = template.Library()


@register.filter
def wrap_words_in_span(value):
    words = re.findall(r'\w+', value)
    wrapped_words = [f'<span>{word}</span>' for word in words]
    return ' '.join(wrapped_words)