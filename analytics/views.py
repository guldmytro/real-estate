from django.shortcuts import render
from .models import Analytic
from django.core.paginator import Paginator, EmptyPage


def analytics_list(request):
    news_list = Analytic.objects.all()
    paginator = Paginator(news_list, 8)
    page_number = request.GET.get('page', 1)
    title = 'Аналітичні огляди'
    try:
        news = paginator.page(page_number)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    context = {
        'news': news,
        'title': title
    }
    return render(request, 'news/list.html', context)


def analytics_detail(request):
    return render(request, 'news/detail.html', {})