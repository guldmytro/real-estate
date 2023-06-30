from django.shortcuts import render
from .models import News
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404


def news_list(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 8)
    page_number = request.GET.get('page', 1)
    title = 'Новини'
    try:
        news = paginator.page(page_number)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    context = {
        'news': news,
        'title': title
    }
    return render(request, 'news/list.html', context)


def news_detail(request, slug):
    post = get_object_or_404(News, slug=slug)
    context = {
        'post': post
    }
    return render(request, 'news/detail.html', context)
