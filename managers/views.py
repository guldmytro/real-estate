from django.shortcuts import render, get_object_or_404
from .models import Manager
from listings.models import Listing


def managers_detail(request, id):
    manager = get_object_or_404(Manager.objects.prefetch_related('phones'), id=id)
    listings = Listing.objects.filter(manager=manager)
    context = {
        'manager': manager,
        'listings': listings
    }
    return render(request, 'managers/detail.html', context)
