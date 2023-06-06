from django.shortcuts import render, get_object_or_404
from .models import Listing, Attribute
from django.db.models import Prefetch


def listings_list(request):
    listings = Listing.active.prefetch_related('images').all()
    context = {
        'listings': listings
    }
    return render(request, 'listings/list.html', context)


def listings_detail(request, id):
    listing = get_object_or_404(
        Listing.objects.prefetch_related(
            Prefetch('images'),
            Prefetch('kits__attribute', queryset=Attribute.objects.order_by('-title'))
        ).select_related('manager'),
        id=id
    )
    in_wishlist = str(id) in request.COOKIES.get('wishlist', '').split(',')
    context = {
        'listing': listing,
        'in_wishlist': in_wishlist
    }
    return render(request, 'listings/item.html', context)
