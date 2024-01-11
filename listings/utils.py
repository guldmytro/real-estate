from .models import Listing, Kit, City, Street, Country, RealtyType, Category, Image, District, HouseComplex
from managers.models import Manager
from django.db.models import Count
import requests, uuid
from props.models import SiteConfiguration
import os
import shutil
from django.conf import settings
from dateutil.parser import parse
import pytz
import logging
from decimal import Decimal
from django.contrib.gis.geos import Polygon
from django.db.models import Q

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('translation.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


languages_old = {'en': 'en_US', 'uk': 'uk_UA'}

languages = {'en': 'en', 'uk': 'uk', 'ru': 'ru'}


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
    
    street_ids = None
    if cleaned_data.get('street'):
        street_ids = [int(id) for id in cleaned_data.get('street').split(',')]
    
    house_complex_ids = None
    if cleaned_data.get('house_complex'):
        house_complex_ids = [int(id) for id in cleaned_data.get('house_complex').split(',')]

    district_ids = None
    if cleaned_data.get('district'):
        district_ids = [int(id) for id in cleaned_data.get('district').split(',')]

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

    min_area = cleaned_data.get('min_area')
    max_area = cleaned_data.get('max_area')
    floor_from = cleaned_data.get('floor_from')
    floor_to = cleaned_data.get('floor_to')
    floors_from = cleaned_data.get('floors_from')
    floors_to = cleaned_data.get('floors_to')
    with_photo = cleaned_data.get('with_photo')
    with_video = cleaned_data.get('with_video')
    is_new_building = cleaned_data.get('is_new_building')
    polygon = cleaned_data.get('polygon')

    if is_new_building:
        listings = listings.filter(is_new_building=True)

    if deal:
        listings = listings.filter(deal=deal)

    loc_q = Q()

    if street_ids:
        loc_q |= Q(street_id__in=street_ids)
    
    if district_ids:
        loc_q |= Q(district_id__in=district_ids)

    if house_complex_ids:
        loc_q |= Q(house_complex_id__in=house_complex_ids)

    listings = listings.filter(loc_q)
        
    

    if number_of_rooms:
        q_rooms = Q()
        if '4+' in number_of_rooms:
            q_rooms |= Q(room_count__gte=4)
            number_of_rooms.remove('4+')
        if len(number_of_rooms):
            q_rooms |= Q(room_count__in=number_of_rooms)
        listings = listings.filter(q_rooms)

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

    if min_area:
        listings = listings.filter(area_total__gte=min_area)
        
    if max_area:
        listings = listings.filter(area_total__lte=max_area)

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

    if polygon:
        polygon_coordinates = tuple(tuple(Decimal(coord) for coord in point.split(',')) for point in polygon.split(';'))
        polygon_coordinates += (polygon_coordinates[0],)
        polygon_obj = Polygon(polygon_coordinates)
        listings = listings.filter(coordinates__within=polygon_obj)
        
    return listings


def get_similar_listings(listing):
    city = None
    try:
        city = listing.street.city
    except:
        pass

    similar_listings = Listing.objects.filter(
        street__city=city,
        room_count=listing.room_count,
        deal=listing.deal,
        realty_type=listing.realty_type,
        price__gte=listing.price - 10000,
        price__lte=listing.price + 10000
    ).exclude(id=listing.id)

    similar_listings = similar_listings[:10]

    return similar_listings


def modify_get(GET):
    modified_get = GET.copy()
    modified_get['address_input'] = ''
    return modified_get


def get_listings_map_data(listings):
    coordinates = [{
        'id': listing.pk,
        'lat': listing.coordinates.y, 
        'lng': listing.coordinates.x,
        'price': listing.formated_price(),
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
            translated_text = response['translations'][0].get('text', text)
            logger.info(f"Translated '{text}' from {from_lang} to {to_lang}: {translated_text}")
            return translated_text
        except:
            logger.warning(f"Translation response format is not as expected: {response}")
            return text
    except requests.exceptions.RequestException as e:
        logger.error(f"Translation error with translating phrase '{text}': {e}")
        return text


def clear_database():
    Image.objects.all().delete()
    Listing.objects.all().delete()
    Country.objects.all().delete()
    RealtyType.objects.all().delete()
    Category.objects.all().delete()
    Manager.objects.all().delete()
    Kit.objects.all().delete()

    folder_path = os.path.join(settings.MEDIA_ROOT, 'listings')

    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f'Папка {folder_path} успішно видалена.')
        except OSError as e:
            print(f'Помилка при видаленні папки {folder_path}: {e}')
    else:
        print(f'Папки {folder_path} не існує.')


def convert_to_utc(date_string):
    local_time = parse(date_string)

    if local_time.tzinfo is None:
        local_time = local_time.replace(tzinfo=pytz.UTC)

    utc_time = local_time.astimezone(pytz.UTC)

    return utc_time


def get_current_city(request):
    city_id = request.session.get('current_city', False)
    if not city_id:
        return None
    try:
        city = City.objects.get(pk=city_id)
        return city
    except City.DoesNotExist:
        return None
    

def get_addresses_dict(cd):
    street = cd.get('street')
    district = cd.get('district')
    house_complex = cd.get('house_complex')
    result = []

    if street:
        street_ids = [int(id) for id in street.split(',')]
        for street in Street.objects.filter(id__in=street_ids):
            result.append({
                'value': street.id,
                'name': 'street',
                'label': street.title
            })
    

    if district:
        district_ids = [int(id) for id in district.split(',')]
        for disrict in District.objects.filter(id__in=district_ids):
            result.append({
                'value': disrict.id,
                'name': 'disrict',
                'label': disrict.title
            })


    if house_complex:
        house_complex_ids = [int(id) for id in house_complex.split(',')]
        for house_complex in HouseComplex.objects.filter(id__in=house_complex_ids):
            result.append({
                'value': house_complex.id,
                'name': 'house_complex',
                'label': house_complex.title
            })

    return result
    
