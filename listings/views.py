from django.shortcuts import render, get_object_or_404
from .models import Listing, Attribute
from django.db.models import Prefetch
from django.contrib.gis.measure import Distance
from news.models import News
from django.template.loader import render_to_string


def listings_list(request):
    listings = Listing.active.prefetch_related('images').all()
    coordinates = [{
        'lat': listing.coordinates.y, 
        'lng': listing.coordinates.x,
        'content': render_to_string('listings/components/listing-map-info.html', {'listing': listing, 'year': listing.kits.filter(attribute__slug='property_23')})
        } for listing in listings]
    context = {
        'listings': listings,
        'coordinates': coordinates
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

    listings_the_same_street_num = Listing.active.prefetch_related(
        Prefetch('images')
    ).select_related('manager').filter(
        street_number=listing.street_number, street=listing.street
    ).exclude(id=listing.id)[:10]

    listings_within_distance = Listing.active.prefetch_related(
        Prefetch('images')
    ).select_related('manager').filter(
        coordinates__distance_lte=(listing.coordinates, Distance(m=5000))
    ).exclude(
        street_number=listing.street_number, street=listing.street
    )[:10]

    news = News.objects.all()[:8]

    context = {
        'listing': listing,
        'in_wishlist': in_wishlist,
        'listings_the_same_street_num': listings_the_same_street_num,
        'listings_within_distance': listings_within_distance,
        'news': news
    }

    return render(request, 'listings/item.html', context)
