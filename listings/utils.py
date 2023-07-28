from .models import Listing, Kit, City, Street, Country, RealtyType, Category
from managers.models import Manager
from django.template.loader import render_to_string
from django.db.models import Count
import requests, uuid
from props.models import SiteConfiguration


languages_old = {'en': 'en_US', 'uk': 'uk_UA'}

languages = {'en': 'en', 'uk': 'uk'}


translation_key = None
translation_location = None
try:
    config = SiteConfiguration.objects.get()
    translation_key = config.azure_secret_key
    translation_location = config.azure_location
except:
    config = False


def filter_listings(cleaned_data, listings):
    deal = cleaned_data.get('deal')
    city_id = cleaned_data.get('city')
    street_id = cleaned_data.get('street')
    number_of_rooms = cleaned_data.get('number_of_rooms')
    min_price = cleaned_data.get('min_price')
    max_price = cleaned_data.get('max_price')
    realty_type = cleaned_data.get('realty_type')

    repair = cleaned_data.get('repair')
    planning = cleaned_data.get('planning')
    listing_class = cleaned_data.get('listing_class')
    floor = cleaned_data.get('floor')
    windows = cleaned_data.get('windows')
    enter = cleaned_data.get('enter')
    outside_decorating = cleaned_data.get('outside_decorating')
    floor_from = cleaned_data.get('floor_from')
    floor_to = cleaned_data.get('floor_to')
    floors_from = cleaned_data.get('floors_from')
    floors_to = cleaned_data.get('floors_to')
    with_photo = cleaned_data.get('with_photo')
    with_video = cleaned_data.get('with_video')
    is_new_building = cleaned_data.get('is_new_building')

    if is_new_building:
        listings = listings.filter(is_new_building=True)

    if deal:
        listings = listings.filter(deal=deal)

    if street_id:
        listings = listings.filter(street_id=street_id)
    elif city_id:
        listings = listings.filter(street__city_id=city_id)
    
    if number_of_rooms:
        if number_of_rooms == '4+':
            listings = listings.filter(room_count__gte=4)
        else:
            listings = listings.filter(room_count=number_of_rooms)

    if min_price and max_price:
        listings = listings.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        listings = listings.filter(price__gte=min_price)
    elif max_price:
        listings = listings.filter(price__lte=max_price)

    if realty_type:
        listings = listings.filter(realty_type=realty_type)

    if repair:
        listings = listings.filter(kits=repair)

    if planning:
        listings = listings.filter(kits=planning)

    if listing_class:
        listings = listings.filter(kits=listing_class)

    if floor:
        listings = listings.filter(kits=floor)

    if windows:
        listings = listings.filter(kits=windows)

    if enter:
        listings = listings.filter(kits=enter)

    if outside_decorating:
        listings = listings.filter(kits=outside_decorating)

    if floor_from:
        listings = listings.filter(floor__gte=floor_from)
        
    if floor_to:
        listings = listings.filter(floor__lte=floor_to)

    if floors_from:
        listings = listings.filter(total_floors__gte=floors_from)

    if floors_to:
        listings = listings.filter(total_floors__lte=floors_to)

    if with_photo:
        listings = listings.annotate(photo_cnt=Count('images')).filter(photo_cnt__gte=1)

    if with_video:
        listings = listings.exclude(video_url__isnull=True)
        
    return listings


def get_similar_listings(listing):
    city = None
    try:
        city = listing.street.city
    except:
        pass
    room_count = listing.room_count

    similar_listings = Listing.objects.filter(
        street__city=city,
        room_count=room_count,
    ).exclude(id=listing.id)


    try: 
        kit = Kit.objects.get(attribute__slug='property_23', listing=listing)
        year_built = int(kit.value)

        min_year_built = year_built - 3
        max_year_built = year_built + 3

        similar_listings = similar_listings.filter(
            kits__attribute__slug='property_23',
            kits__translations__value__gte=str(min_year_built),
            kits__translations__value__lte=str(max_year_built),
        )
    except Kit.DoesNotExist:
        pass

    similar_listings = similar_listings[:10]

    return similar_listings


def modify_get(GET):
    modified_get = GET.copy()
    city = modified_get.get('city')
    street = modified_get.get('street')
    try:
        if city:
            city_obj = City.objects.get(id=city)
            if city_obj.region:
                modified_get['address_input'] = f'{city_obj.title} ({city_obj.region.title})'
            else:
                modified_get['address_input'] = city_obj.title
        elif street:
            street_obj = Street.objects.get(id=street)
            try:
                modified_get['address_input'] = f'{street_obj.title} ({street_obj.city.title}, {street_obj.city.region.title})'
            except:
                modified_get['address_input'] = f'{street_obj.title} ({street_obj.city.title})'
    except:
        pass
    return modified_get


def get_listings_map_data(listings):
    coordinates = [{
        'lat': listing.coordinates.y, 
        'lng': listing.coordinates.x,
        'price': listing.formated_price(),
        'content': render_to_string(
        'listings/components/listing-map-info.html', {
            'listing': listing, 
            'year': listing.kits.filter(attribute__slug='property_23')
            })
        } for listing in listings]
    return coordinates
    

def translate(text, from_lang=None, to_lang=None):
    if not text:
        return text
    endpoint = "https://api.cognitive.microsofttranslator.com"

    
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': [to_lang]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': translation_key,
        'Ocp-Apim-Subscription-Region': translation_location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        request.raise_for_status()
        response = request.json()[0]
        if not 'translations' in response:
            return text
        try:
            return response['translations'][0].get('text', text)
        except:
            return text
    except requests.exceptions.RequestException as e:
        print(f"Translation error with translating phrase {text}: {e}")
        return text


def clear_database():
    Listing.objects.all().delete()
    Country.objects.all().delete()
    RealtyType.objects.all().delete()
    Category.objects.all().delete()
    Manager.objects.all().delete()
    Kit.objects.all().delete()

