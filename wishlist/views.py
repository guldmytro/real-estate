from django.shortcuts import render
from listings.models import Listing
from django.core.paginator import Paginator, EmptyPage


def wishlist_archive(request):
    ids = list(filter(lambda id: id != '', request.COOKIES.get('wishlist', '').split(',')))
    listings_list = Listing.active.prefetch_related('images').filter(id__in=ids)
    paginator = Paginator(listings_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        listings = paginator.page(page_number)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)
    context = {
        'listings': listings
    }
    return render(request, 'wishlist/list.html', context)
