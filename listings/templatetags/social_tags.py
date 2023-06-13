from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def telegram(context, title):
    request = context['request']
    url = request.build_absolute_uri()
    return f'https://telegram.me/share/url?text={title}&url={url}'


@register.simple_tag(takes_context=True)
def facebook(context):
    request = context['request']
    url = request.build_absolute_uri()
    return f'https://www.facebook.com/sharer/sharer.php?u={url}'


@register.simple_tag(takes_context=True)
def viber(context):
    request = context['request']
    url = request.build_absolute_uri()
    return f'viber://forward?text={url}'


@register.simple_tag(takes_context=True)
def twitter(context):
    request = context['request']
    url = request.build_absolute_uri()
    return f'https://twitter.com/intent/tweet?url={url}'

