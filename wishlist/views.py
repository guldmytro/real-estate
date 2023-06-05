from django.shortcuts import render
from listings.models import Listing


def wishlist_archive(request):
    ids = list(filter(lambda id: id != '', request.COOKIES.get('wishlist', '').split(',')))
    print(ids)
    listings = Listing.objects.filter(id__in=ids)
    context = {
        'listings': listings
    }
    return render(request, 'wishlist/list.html', context)
