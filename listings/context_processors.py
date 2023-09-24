from .models import RealtyType, Listing, City
from django.db.models import Count
from django.shortcuts import redirect


def real_types(request):
    real_types = RealtyType.objects.annotate(cnt=Count('listings'))\
        .filter(cnt__gt=0).exclude(translations__menu_label__isnull=True)\
        .order_by()
    return {'real_types': real_types}


def wishlist_types(request):
    ids = list(filter(lambda id: id != '', request.COOKIES.get('wishlist', '').split(',')))
    wishlist_count = Listing.objects.filter(id__in=ids).count()
    if wishlist_count > 9:
        wishlist_count = '9+'
    return {'wishlist_count': wishlist_count}

def cities(request):
    cities_qs = City.objects.annotate(cnt=Count('streets__listings'))\
        .filter(cnt__gte=1,
                translations__language_code=request.LANGUAGE_CODE)\
        .order_by('translations__title')
    current_city_pk = request.session.get('current_city', False)
    current_city = None
    if current_city_pk:
        try: 
            current_city = City.objects.get(pk=current_city_pk)
        except City.DoesNotExist:
            pass

    cities_obj = {}
    for city in cities_qs:
        first_letter = city.title[0].upper()
        if first_letter not in cities_obj:
            cities_obj[first_letter] = []
        cities_obj[first_letter].append(city)
    return {'cities_obj': cities_obj,
            'current_city': current_city}