from django.shortcuts import render, get_object_or_404
from .models import Manager, Review
from listings.models import Listing

POSTS_PER_PAGE = 8


def managers_detail(request, id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        return managers_detail_pagination(request, id)

    manager = get_object_or_404(Manager.objects.prefetch_related('phones'), id=id)
    listings = Listing.objects.order_by('-created').filter(manager=manager)[:POSTS_PER_PAGE]
    reviews = Review.objects.order_by('-created').filter(manager=manager)[:POSTS_PER_PAGE]
    context = {
        'manager': manager,
        'listings': listings,
        'listings_count': Listing.objects.count(),
        'reviews': reviews,
        'reviews_count': Review.objects.count(),
    }
    return render(request, 'managers/detail.html', context)


def managers_detail_pagination(request, id):
    manager = get_object_or_404(Manager, id=id)
    items = None
    next_page = None
    start_pos = int(request.GET.get('page', 1)) * POSTS_PER_PAGE - POSTS_PER_PAGE
    end_pos = start_pos + POSTS_PER_PAGE
    max_items = 0
    if request.GET.get('type', '') == 'review':
        max_items = Review.objects.filter(manager=manager).count()
        items = Review.objects.order_by('-created').filter(manager=manager)[start_pos:end_pos]
    if request.GET.get('type', '') == 'listing':
        max_items = Listing.objects.filter(manager=manager).count()
        items = Listing.objects.order_by('-created').filter(manager=manager)[start_pos:end_pos]
    if items:
        next_page = int(request.GET.get('page', 1)) + 1 if max_items > end_pos else None
    context = {
        'type': request.GET.get('type', ''),
        'items': items,
        'next_page': next_page
    }
    return render(request, 'ajax-items.html', context)


def managers_list(request):
    return render(request, 'managers/detail.html', {})