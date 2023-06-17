from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Listing, Attribute, City, Street
from django.db.models import Prefetch, Count
from django.contrib.gis.measure import Distance
from news.models import News
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
import json
from .utils import filter_listings



def listings_list(request):
    search_form = SearchForm(request.GET)
    listings_list = Listing.active.prefetch_related('images').all()
    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        listings_list = filter_listings(cleaned_data, listings_list)
    else:
        print('invalid')
    coordinates = [{
        'lat': listing.coordinates.y, 
        'lng': listing.coordinates.x,
        'price': listing.formated_price(),
        'content': render_to_string(
        'listings/components/listing-map-info.html', {
            'listing': listing, 
            'year': listing.kits.filter(attribute__slug='property_23')
            })
        } for listing in listings_list]
    
    paginator = Paginator(listings_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        listings = paginator.page(page_number)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)
        
    context = {
        'listings': listings,
        'count': listings_list.count(),
        'coordinates': coordinates,
        'search_form': search_form
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


def get_listings_count(request):
    search_form = SearchForm(request.GET)
    listings_list = Listing.active.prefetch_related('images').all()
    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        listings_list = filter_listings(cleaned_data, listings_list)
    return JsonResponse({'success': True, 'count': listings_list.count()})


@require_POST
def get_address_predictions(request):
    body_data = json.loads(request.body)
    search_query = body_data.get('search_query', '')

    cities = City.objects.annotate(
        cnt=Count('streets'),
        similarity=TrigramSimilarity('title', search_query)
    ).filter(similarity__gt=0.15, cnt__gt=0).order_by('-similarity')[:10]

    streets = Street.objects.annotate(
        cnt=Count('listings'),
        similarity=TrigramSimilarity('title', search_query)
    ).filter(similarity__gt=0.15, cnt__gt=0).order_by('-similarity')[:10]

    return JsonResponse({
        'status': 'ok',
        'cities': [{'title': city.title, 'id': city.pk} for city in cities],
        'streets': [{'title': street.title, 'id': street.pk, 
                     'related_city': {'title': street.city.title, 'id': street.city.pk}} for street in streets],
        })
