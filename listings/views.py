from django.shortcuts import render, get_object_or_404
from .models import Listing


def listings_list(request):
    listings = Listing.active.prefetch_related('images').all()
    context = {
        'listings': listings
    }
    return render(request, 'listings/list.html', context)


def listings_detail(request, id):
    listing = get_object_or_404(Listing.objects.prefetch_related('images'), id=id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/item.html', context)
