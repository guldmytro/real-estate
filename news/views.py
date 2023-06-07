from django.shortcuts import render


def news_list(request):
    return ''


def news_detail(request, slug):
    return render(request, 'news/item.html', {})
