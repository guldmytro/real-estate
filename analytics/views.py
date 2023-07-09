from django.shortcuts import render
from .models import Analytic
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def analytics_list(request):
    news_list = Analytic.objects.all().order_by('-created')
    paginator = Paginator(news_list, 8)
    page_number = request.GET.get('page', 1)
    title = _('Analytical reviews')
    try:
        news = paginator.page(page_number)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    crumbs = [
        (_('Analytical reviews'), reverse_lazy('analytics:list'))
    ]
    context = {
        'news': news,
        'title': title,
        'crumbs': crumbs
    }
    return render(request, 'news/list.html', context)


def analytics_detail(request, id):
    post = get_object_or_404(Analytic, id=id)
    crumbs = [
        (_('Analytical reviews'), reverse_lazy('analytics:list')),
        (post.title, post.get_absolute_url),
    ]
    context = {
        'post': post,
        'crumbs': crumbs
    }
    return render(request, 'news/detail.html', context)