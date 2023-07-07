from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Listing, Attribute, City, Street
from django.db.models import Prefetch, Count
from django.contrib.gis.measure import Distance
from news.models import News
from django.core.paginator import Paginator, EmptyPage
from .forms import SearchForm, SearchFormSimplified
from django.contrib.postgres.search import TrigramSimilarity
import json
from .utils import filter_listings, get_similar_listings, modify_get, get_listings_map_data
from emails.forms import ListingPhoneForm, ListingMessageForm, \
    ListingVisitForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def listings_list(request):
    GET = modify_get(request.GET)
    search_form = SearchForm(GET)
    listings_list = Listing.active.prefetch_related('images').all()
    crumbs = []

    # Filtering
    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        
        city = cleaned_data.get('city')
        street = cleaned_data.get('street')
        address = cleaned_data.get('address')

        if city:
            try:
                city = City.objects.get(id=city)
                crumb_title = city.title
            except: 
                crumb_title = ''
        if street:
            try:
                street = Street.objects.get(id=street)
                city = street.city
                crumb_title = f'{street.title} ({city.title})'
            except: 
                crumb_title = ''
        
        if not city and not street:
            try:
                cities_with_count = City.objects.annotate(listing_count=Count('streets__listings'))
                cities_with_count = cities_with_count.order_by('-listing_count')
                city = cities_with_count.first()
                address = City.title
                crumb_title = city.title
            except:
                pass

        crumbs.append(
            (_('Listings') + f' {crumb_title}', reverse_lazy('listings:list'))
        )
            
            
        cleaned_data['city'] = city
        cleaned_data['address'] = address
        listings_list = filter_listings(cleaned_data, listings_list)
    else:
        listings_list = Listing.objects.none()
    
    # Parsing listing coordinates for GoogleMaps
    coordinates = get_listings_map_data(listings_list)
    

    # Pagination
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
        'search_form': search_form,
        'crumbs': crumbs,
    }
    return render(request, 'listings/list.html', context)


def listings_detail(request, id):
    listing = get_object_or_404(
        Listing.objects.prefetch_related(
            Prefetch('images'),
            Prefetch('kits__attribute', queryset=Attribute.objects.order_by('-title'))
        ).select_related('manager').select_related('street'),
        id=id
    )
    crumbs = []

    if listing.street:
        crumbs.append(
            (_('Listings') + f' {listing.street.city.title}', listing.street.city.get_absolute_url())
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

    similar_listings = get_similar_listings(listing)

    news = News.objects.all()[:8]

    crumbs.append(
        (listing.title, listing.get_absolute_url())
    )

    # forms
    listing_phone_form = ListingPhoneForm()
    listing_message_form = ListingMessageForm()
    listing_visit_form = ListingVisitForm()

    context = {
        'listing': listing,
        'in_wishlist': in_wishlist,
        'listings_the_same_street_num': listings_the_same_street_num,
        'listings_within_distance': listings_within_distance,
        'news': news,
        'listing_phone_form': listing_phone_form,
        'listing_message_form': listing_message_form,
        'listing_visit_form': listing_visit_form,
        'similar_listings': similar_listings,
        'crumbs': crumbs
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
        cnt=Count('streets__listings'),
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


def get_listings_coordinates(request):
    search_form_simplified = SearchFormSimplified(request.GET)
    if search_form_simplified.is_valid():
        cd = search_form_simplified.cleaned_data
        city = cd['city']
        street = cd['street']
        if city or street:
            listings_list = Listing.active.prefetch_related('images').all()
            listings_list = filter_listings(cd, listings_list)
            
            # Parsing listing coordinates for GoogleMaps
            coordinates = get_listings_map_data(listings_list)
            return JsonResponse({'success': True, 'coordicates': coordinates})    
    return JsonResponse({'success': False})
