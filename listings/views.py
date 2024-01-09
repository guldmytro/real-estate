from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Listing, City, Street, Kit, District, HouseComplex, RealtyType, Deal
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
from django.template.loader import render_to_string
from .utils import get_current_city


def listings_list(request, realty_type=None, realty_deal=None): 
    current_city = get_current_city(request)
    r_type = None
    r_deal = None
    GET = modify_get(request.GET)
    search_form = SearchForm(GET)

    listings_list = Listing.objects.prefetch_related(
        Prefetch('images'),
        Prefetch('kits__attribute'),
    ).all()


    if current_city is not None:
        listings_list = listings_list.filter(street__city=current_city)

    if realty_type:
        if realty_type == 'new':
            listings_list = listings_list.filter(is_new_building=True)
            r_type = {}
            r_type['menu_label'] = _('New buildings')
            r_type['slug'] = 'new'
        else:
            r_type = get_object_or_404(RealtyType, slug=realty_type)  
            listings_list = listings_list.filter(realty_type=r_type)
    if realty_deal:
        if realty_deal == 'buy':
            r_deal = get_object_or_404(Deal, title='Продаж')
        elif realty_deal == 'rent':
            r_deal = get_object_or_404(Deal, title='Оренда')
        listings_list = listings_list.filter(deal=r_deal)

    crumbs = []

    # Filtering
    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        
        city = cleaned_data.get('city')
        street = cleaned_data.get('street')
        address = cleaned_data.get('address')
        district = cleaned_data.get('district')
        house_complex = cleaned_data.get('house_complex')
        crumb_title = False

        # if not city and not street and not district and not house_complex:
        #     try:
        #         cities_with_count = City.objects.annotate(listing_count=Count('streets__listings'))
        #         cities_with_count = cities_with_count.order_by('-listing_count')
        #         city = cities_with_count.first()
        #         if city:
        #             query_params = request.GET.copy()
        #             query_params['city'] = city.id
        #             url = request.path + '?' + query_params.urlencode()
        #             return redirect(url)
        #     except:
        #         pass
            
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
        if district:
            try:
                district = District.objects.get(id=district)
                crumb_title = district.title
            except: 
                crumb_title = ''
        if house_complex:
            try:
                house_complex = HouseComplex.objects.get(id=house_complex)
                crumb_title = house_complex.title
            except: 
                crumb_title = ''
        

    
        if crumb_title:
            crumbs.append(
                (_('Listings') + f' {crumb_title}', reverse_lazy('listings:list'))
            )
            
            
        cleaned_data['city'] = city
        cleaned_data['address'] = address
        listings_list = filter_listings(cleaned_data, listings_list)
    else:
        listings_list = Listing.objects.none()
    

    
    # Pagination
    paginator = Paginator(listings_list, 20)
    page_number = request.GET.get('page', 1)
    try:
        listings = paginator.page(page_number)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)
    
    # Parsing listing coordinates for GoogleMaps
    coordinates = get_listings_map_data(listings_list)
    

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        res = JsonResponse({
            'html': render_to_string('listings/list-ajax.html', {'request': request,
                                                                 'listings': listings}),
            'count': listings_list.count(),
            'coordinates': coordinates
        })
        res['Cache-Control'] = 'no-store'
        return res
    
    context = {
        'listings': listings,
        'count': listings_list.count(),
        'coordinates': coordinates,
        'search_form': search_form,
        'crumbs': crumbs,
        'realty_type': r_type,
        'realty_deal': r_deal
    }
    return render(request, 'listings/list.html', context)


def listings_detail(request, id):
    listing = get_object_or_404(
        Listing.objects.prefetch_related(
            Prefetch('images'),
        ).select_related('manager').select_related('street'),
        id=id,
    )

    kits = Kit.objects.select_related('attribute').filter(listing=listing).order_by()

    crumbs = []

    if listing.street:
        try:
            crumbs.append(
                (_('Listings') + f' {listing.street.city.title}', listing.street.city.get_absolute_url())
            )
        except:
            pass

    in_wishlist = str(id) in request.COOKIES.get('wishlist', '').split(',')

    listings_the_same_street_num = Listing.objects.prefetch_related(
        Prefetch('images')
    ).select_related('manager').filter(
        street_number=listing.street_number, street=listing.street
    ).exclude(id=listing.id)[:10]
    
    listings_within_distance = Listing.objects.prefetch_related(
        Prefetch('images')
    ).select_related('manager').filter(
        coordinates__distance_lte=(listing.coordinates, Distance(m=2000)),
        deal=listing.deal,
        room_count=listing.room_count,
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
        'kits': kits,
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


def get_listings_count(request, realty_type=None, realty_deal=None):
    search_form = SearchForm(request.GET)
    listings_list = Listing.objects.prefetch_related('images').all()
    current_city = get_current_city(request)
    if current_city is not None:
        listings_list = listings_list.filter(street__city=current_city)
    
    if realty_type:
        if realty_type == 'new':
            listings_list = listings_list.filter(is_new_building=True)
        else:
            r_type = get_object_or_404(RealtyType, slug=realty_type)
            listings_list = listings_list.filter(realty_type=r_type)
    
    if realty_deal:
        if realty_deal == 'buy':
            r_deal = get_object_or_404(Deal, title='Продаж')
        elif realty_deal == 'rent':
            r_deal = get_object_or_404(Deal, title='Оренда')
        listings_list = listings_list.filter(deal=r_deal)

    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        listings_list = filter_listings(cleaned_data, listings_list)
    return JsonResponse({'success': True, 'count': listings_list.count()})


@require_POST
def get_address_predictions(request):
    current_city = get_current_city(request)
    body_data = json.loads(request.body)
    search_query = body_data.get('search_query', '')

    cities = City.objects.annotate(
        cnt=Count('streets__listings'),
        similarity=TrigramSimilarity('translations__title', search_query)
    ).filter(similarity__gt=0.15, cnt__gt=0).order_by('-similarity')

    streets = Street.objects.annotate(
        cnt=Count('listings'),
        similarity=TrigramSimilarity('translations__title', search_query)
    ).filter(similarity__gt=0.15, cnt__gt=0).order_by('-similarity')

    districts = District.objects.annotate(
        cnt=Count('listings'),
        similarity=TrigramSimilarity('translations__title', search_query)
    ).filter(similarity__gt=0.15, cnt__gt=0).order_by('-similarity')

    house_compexes = HouseComplex.objects.annotate(
        cnt=Count('listings'),
        similarity=TrigramSimilarity('translations__title', search_query)
    ).filter(similarity__gt=0.15, cnt__gt=0).order_by('-similarity')

    if current_city is not None:
        streets = streets.filter(city=current_city)
        districts = districts.filter(city=current_city)
        house_compexes = house_compexes.filter(city=current_city)

    return JsonResponse({
        'status': 'ok',
        'cities': [{'title': city.title, 'id': city.pk,
                    'related_region': {'title': city.region.title} \
                        if hasattr(city, 'region') else None,} for city in cities],
        'streets': [{'title': street.title, 'id': street.pk, 
                     'related_city': {'title': street.city.title, 'id': street.city.pk},
                     'related_region': {'title': street.city.region.title} \
                          if hasattr(street.city, 'region') else None,} \
                              for street in streets],
        'districts': [{'title': district.title, 'id': district.pk, 
                     'related_city': {'title': district.city.title, 'id': district.city.pk},
                     'related_region': {'title':district.city.region.title} \
                          if hasattr(district.city, 'region') else None,} \
                              for district in districts],
        'house_complexes': [{'title': house_complex.title, 'id': house_complex.pk, 
                     'related_city': {'title': house_complex.city.title, 'id': house_complex.city.pk},
                     'related_region': {'title':house_complex.city.region.title} \
                          if hasattr(house_complex.city, 'region') else None,} \
                              for house_complex in house_compexes],
        })
        


def get_listings_coordinates(request):
    search_form_simplified = SearchFormSimplified(request.GET)
    if search_form_simplified.is_valid():
        cd = search_form_simplified.cleaned_data
        street = cd['street']
        district = cd['district']
        house_complex = cd['house_complex']
        if street or district or house_complex:
            listings_list = Listing.objects.all()
            listings_list = filter_listings(cd, listings_list)
            
            # Parsing listing coordinates for GoogleMaps
            coordinates = get_listings_map_data(listings_list)
            return JsonResponse({'success': True, 'coordicates': coordinates})    
    return JsonResponse({'success': False})


@require_POST
def listing_detail_map(request, listing_id):
    listing = get_object_or_404(Listing.objects.prefetch_related(
        Prefetch('images'),
        Prefetch('kits__attribute')
    ), id=listing_id)
    return JsonResponse({'html': render_to_string(
        'listings/components/listing-map-info.html', {
            'listing': listing,
            'year': listing.kits.filter(attribute__slug='property_23')}
    )})
