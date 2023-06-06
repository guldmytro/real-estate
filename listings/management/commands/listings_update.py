from django.core.management.base import BaseCommand
from props.models import SiteConfiguration
import requests
import xml.etree.ElementTree as ET
import json
import re
from django.utils.html import strip_tags
from listings.models import Listing, Category, RealtyType, \
    Image, Kit, Attribute, Country, City, Street
from managers.models import Manager, Phone
from django.contrib.gis.geos import Point
from django.utils.text import slugify


config = SiteConfiguration.objects.get()
CRM_API = config.crm_api
GOOGLE_API_KEY = config.google_api_key


class Command(BaseCommand):
    help = 'Update listings from Feed API'

    def handle_from_api(self, *args, **options):
        response = requests.get(CRM_API)

        # Bad request
        if response.status_code != 200:
            return False

        # Everything is ok, parsing
        xml_data = response.text
        root = ET.fromstring(xml_data)

        items = []
        for item in root:
            items.append(self.parse_item(item))
        with open('result.json', 'w', encoding='utf-8') as json_file:
            json.dump(items, json_file, indent=4, ensure_ascii=False)
        self.update_models(items)

    def handle(self, *args, **options):
        with open('result.json', encoding='utf-8') as json_file:
            items = json.load(json_file)
        self.update_models(items)

    def parse_item(self, item):
        item_dict = {
            'id': item.get('internal-id')
        }
        for child in item:
            if child.tag == 'location':
                location = {}
                for location_child in child:
                    location[location_child.tag] = self.clear_string(location_child.text)
                item_dict[child.tag] = location
            elif child.tag == 'images':
                images = []
                for image_url in child.iter('image_url'):
                    images.append(self.clear_string(image_url.text))
                item_dict[child.tag] = images
            elif child.tag == 'properties':
                properties = []
                for property_elem in child.iter('property'):
                    property_dict = {
                        'id': self.clear_string(property_elem.get('attribute')),
                        'label': self.clear_string(property_elem.get('label')),
                        'value': self.clear_string(property_elem.text)
                    }
                    properties.append(property_dict)
                item_dict[child.tag] = properties
            elif child.tag == 'user':
                user_data = {}
                for user_elem in child:
                    if user_elem.tag == 'phones':
                        phones = []
                        for phone_elem in user_elem:
                            phones.append(self.clear_string(phone_elem.text))
                        user_data[user_elem.tag] = phones
                    else:
                        user_data[user_elem.tag] = self.clear_string(user_elem.text)
                item_dict[child.tag] = user_data
            else:
                item_dict[child.tag] = self.clear_string(child.text)
        return item_dict

    def clear_string(self, str):
        if str is not None:
            return strip_tags(re.sub(r'^\s+|\s+$|\s+(?=\s)', '', str))
        return str

    def fetch_geo_data(self, lng, lat):
        response = requests.get(
            f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_API_KEY}&language=en')
        if response.status_code != 200:
            return False
        response_json = json.loads(response.text)

        # Extract country
        country = next(
            (component for component in response_json['results'][0]['address_components'] if
             'country' in component['types']),
            None
        )
        country_title = country['long_name'] if country else None

        # Extract city
        city = next(
            (component for component in response_json['results'][0]['address_components'] if
             'locality' in component['types']),
            None
        )
        city_title = city['long_name'] if city else None

        # Extract city coordinates
        city_coordinates = next(
            (component for component in response_json['results'] if
             'postal_code' in component['types']),
            None
        )
        city_coordinates_lat = city_coordinates['geometry']['location']['lat']
        city_coordinates_lng = city_coordinates['geometry']['location']['lng']

        # Extract street
        street = next(
            (component for component in response_json['results'][0]['address_components'] if
             'route' in component['types']),
            None
        )
        street_title = street['long_name'] if street else None

        return {
            'country': {
                'title': country_title
            },
            'city': {
                'title': city_title,
                'lng': city_coordinates_lng,
                'lat': city_coordinates_lat,
            },
            'street': {
                'title': street_title,
            }
        }

    def get_manager(self, user):
        if not user:
            return False

        manager, _ = Manager.objects.get_or_create(
            full_name=user.get('name', ''),
            email=user.get('email', '')
        )
        phones = user.get('phones', [])
        for phone in phones:
            phone_item, _ = Phone.objects.get_or_create(
                manager=manager,
                phone=phone
            )
        # deleting phones that missed in CRM
        for phone in manager.phones.all():
            if phone.phone not in phones:
                phone.delete()

        # Updating Image (if it needs)
        image_url = user.get('image_url', False)
        if not image_url:
            return manager

        if manager.image is None or image_url != manager.image_url:
            try:
                manager.image_url = image_url
                manager.save()
            except:
                pass
        return manager

    def update_models(self, items):
        for data in items:
            # Create or update Category and RealtyType
            category, _ = Category.objects.get_or_create(title=data['category'], slug=slugify(data['category']))
            realty_type, _ = RealtyType.objects.get_or_create(title=data['realty_type'],
                                                              slug=slugify(data['realty_type']))

            # Create Listing object
            listing, _ = Listing.objects.get_or_create(id=int(data['id']))
            listing.status = data['status']
            listing.title = data['title']
            listing.description = data.get('description', '')
            listing.is_new_building = bool(int(data.get('is_new_building', '0')))
            listing.area_total = int(data.get('area_total', '0'))
            listing.area_living = int(data.get('area_living', '0'))
            listing.area_kitchen = int(data.get('area_kitchen', '0'))
            listing.room_count = int(data.get('room_count', '0'))
            listing.floor = int(data.get('floor', '0'))
            listing.total_floors = int(data.get('total_floors', '0'))
            listing.price = int(data.get('price', '0'))
            listing.category = category
            listing.realty_type = realty_type

            lng = float(data['location']['map_lng'])
            lat = float(data['location']['map_lat'])
            listing.coordinates = Point(lng, lat)

            street = None
            # Updating address
            if listing.street is None:
                address_dict = self.fetch_geo_data(float(data['location']['map_lng']),
                                                   float(data['location']['map_lat']))

                if address_dict:
                    street = self.create_listing_address(address_dict)
            if street:
                listing.street = street

            manager = self.get_manager(data.get('user', False))
            if manager:
                listing.manager = manager

            listing.save()

            # Create Images
            for image_url in data['images']:
                image = Image(image_url=image_url, listing=listing)
                try:
                    image.full_clean()
                    image.save()
                except:
                    pass

            # Update images
            for image in listing.images.all():
                if image.image_url not in data['images']:
                    image.delete()

            # Create Kits (Attributes)
            for attribute_data in data['properties']:
                if attribute_data['id'] not in Attribute.BLACKLIST_ATTRIBUTES:
                    attribute, _ = Attribute.objects.get_or_create(title=attribute_data['label'], slug=attribute_data['id'])
                    Kit.objects.get_or_create(listing=listing, attribute=attribute, value=attribute_data['value'])

            # Update listing status
            listing_ids = Listing.objects.values_list('id', flat=True)
            api_ids = {item['id'] for item in items}
            missing_ids = listing_ids.exclude(id__in=api_ids)
            Listing.objects.filter(id__in=missing_ids).update(status='archive')

    def create_listing_address(self, address_dict):
        country, _ = Country.objects.get_or_create(title=address_dict['country']['title'])
        city, _ = City.objects.get_or_create(country=country, title=address_dict['city']['title'],
                                             coordinates=Point(float(address_dict['city']['lng']),
                                                               float(address_dict['city']['lat'])
                                                               )
                                             )
        street, _ = Street.objects.get_or_create(city=city, title=address_dict['street']['title'])
        return street

