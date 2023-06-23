from django.shortcuts import render
from .models import Discount
from django.core.paginator import Paginator, EmptyPage


def discounts_list(request):
    discount_list = Discount.objects.all()
    paginator = Paginator(discount_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        discounts = paginator.page(page_number)
    except EmptyPage:
        discounts = paginator.page(paginator.num_pages)
    context = {
        'discounts': discounts,
    }
    return render(request, 'discounts/list.html', context)


def discounts_detail(request):
    return render(request, 'news/detail.html', {})