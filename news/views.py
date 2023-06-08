from django.shortcuts import render
from .models import News
from django.core.paginator import Paginator, EmptyPage


def news_list(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        news = paginator.page(page_number)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    context = {
        'news': news
    }
    return render(request, 'news/list.html', context)


def news_detail(request, slug):
    return render(request, 'news/item.html', {})
