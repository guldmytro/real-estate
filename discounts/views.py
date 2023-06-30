from django.shortcuts import render
from .models import Discount
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


def discounts_list(request):
    discount_list = Discount.objects.all()
    paginator = Paginator(discount_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        discounts = paginator.page(page_number)
    except EmptyPage:
        discounts = paginator.page(paginator.num_pages)
    crumbs = [
        ('Акції', reverse_lazy('discounts:list')),
    ]
    context = {
        'discounts': discounts,
        'crumbs': crumbs
    }
    return render(request, 'discounts/list.html', context)


def discounts_detail(request, slug):
    post = get_object_or_404(Discount, slug=slug)
    crumbs = [
        ('Акції', reverse_lazy('discounts:list')),
        (post.title, post.get_absolute_url),
    ]
    context = {
        'post': post,
        'crumbs': crumbs
    }
    return render(request, 'news/detail.html', context)