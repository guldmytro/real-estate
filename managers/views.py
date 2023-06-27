from django.shortcuts import render, get_object_or_404
from .models import Manager, Review
from listings.models import Listing
from emails.forms import FeadbackForm, ReviewForm
from django.core.paginator import Paginator, EmptyPage
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity

POSTS_PER_PAGE = 8


def managers_detail(request, id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        return managers_detail_pagination(request, id)
    
    feadback_form = FeadbackForm(request.POST)
    manager = get_object_or_404(Manager.objects.prefetch_related('phones'), id=id)
    review_form = ReviewForm(initial={'manager': manager})
    listings_list = Listing.objects.order_by('-created').filter(manager=manager)
    listings_count = listings_list.count()
    listings = listings_list[:POSTS_PER_PAGE]
    reviews_list = Review.objects.order_by('-created').filter(manager=manager)
    reviews_count = reviews_list.count()
    reviews = reviews_list[:POSTS_PER_PAGE]
    context = {
        'manager': manager,
        'listings': listings,
        'listings_count': listings_count,
        'reviews': reviews,
        'reviews_count': reviews_count,
        'feadback_form': feadback_form,
        'review_form': review_form,
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
    search_form = SearchForm(request.GET)
    managers_list = Manager.objects.prefetch_related('phones').all()
    if search_form.is_valid():
        cd = search_form.cleaned_data
        managers_list = managers_list.annotate(
        similarity=TrigramSimilarity('full_name', cd['full_name']))\
            .filter(similarity__gt=0.15).order_by('-similarity')
    paginator = Paginator(managers_list, 1)
    page_number = request.GET.get('page', 1)
    try:
        managers = paginator.page(page_number)
    except EmptyPage:
        managers = paginator.page(paginator.num_pages)
    context = {
        'managers': managers,
        'search_form': search_form
    }
    return render(request, 'managers/list.html', context)