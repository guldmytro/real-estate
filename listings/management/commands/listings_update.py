from django.core.management.base import BaseCommand
from props.models import SiteConfiguration, Feed
import requests
import xml.etree.ElementTree as ET
import json
import re
from django.utils.html import strip_tags
from listings.models import Listing, Category, RealtyType, Deal, \
    Image, Kit, Attribute, Country, City, Street
from managers.models import Manager, Phone
from django.contrib.gis.geos import Point
from slugify import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from listings.utils import translate, languages
from listings.tasks import add_listing_image, delete_listing_image

validate_url = URLValidator()


config = SiteConfiguration.objects.get()
GOOGLE_API_KEY = config.google_api_key


class Command(BaseCommand):
    help = 'Update listings from Feed API'

    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        if feeds.count():
            self.loop_feeds(feeds)
    
    def loop_feeds(self, feeds):
        for feed in feeds:
            url = feed.feed_url
            response = requests.get(url)

            # Bad request
            if response.status_code != 200:
                continue

            # Everything is ok, parsing
            xml_data = response.text
            root = ET.fromstring(xml_data)

            items = []
            for item in root:
                items.append(self.parse_item(item))
            with open('api-result.json', 'w', encoding='utf-8') as json_file:
                json.dump(items, json_file, indent=4, ensure_ascii=False)

            self.update_models(items)

    def handle_temp(self, *args, **options):
        with open('result.json', encoding='utf-8') as json_file:
            items = json.load(json_file)
            json_file.close()
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

    def fetch_geo_data(self, lng, lat, lang):
        response = requests.get(
            f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_API_KEY}&language={lang}')
        if response.status_code != 200:
            return False
        response_json = json.loads(response.text)
        return self.parse_geo_data(response_json)
    
    def parse_geo_data(self, response_json):

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

        # Extract street
        street = next(
            (component for component in response_json['results'][0]['address_components'] if
             'route' in component['types']),
            None
        )
        street_title = street['long_name'] if street else None

        # Extract street number
        street_num = None
        street_component = next(
            (component for component in response_json['results'] if
             'premise' in component['types']),
            None
        )
        street__items = street_component.get('address_components', None) if street_component else None
        if street__items:
            street_num_dict = next(
                (component for component in street__items if
                 'street_number' in component['types']),
                None
            )
            street_num = street_num_dict.get('short_name', None) if street_num_dict else None

        return {
            'country': {
                'title': country_title,
            },
            'city': {
                'title': city_title,
            },
            'street': {
                'title': street_title,
                'num': street_num
            }
        }

    def get_manager(self, user):
        if not user:
            return False

        email = user.get('email', None)
        name = user.get('name', None)
        if not email:
            return False

        try:
            manager = Manager.objects.get(email=email)
        except Manager.DoesNotExist:
            manager = Manager()
            manager.email = email
            manager.set_current_language('uk')
            manager.full_name = translate(text=name, to_lang=languages['uk'])
            manager.set_current_language('en')
            manager.full_name = translate(text=name, to_lang=languages['en'])
            manager.save()

        if not manager:
            return False
        
        
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
            try: 
                self.add_listing(data)
            except: 
                pass

    def add_listing(self, data):
        # Create or update Category and RealtyType
        category = self.get_category(data.get('category', False))
        realty_type = self.get_realty_type(data.get('realty_type', False))
        deal = self.get_deal(data.get('deal', False))

        # Create Listing object
        listing, _ = Listing.objects.get_or_create(id=int(data['id']))
        listing.status = 'active'
        listing.set_current_language('uk')
        listing.title = data['title']
        listing.description = data.get('description', '')
        listing.set_current_language('en')
        listing.title = translate(data['title'], from_lang=languages['uk'], to_lang=languages['en'])
        listing.description = translate(data.get('description', ''), to_lang=['en'])
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
        listing.deal = deal

        lng = float(data['location']['map_lng'])
        lat = float(data['location']['map_lat'])

        need_update_address = str(lng) != str(listing.get_coordinates_lng()) or \
                                str(lat) != str(listing.get_coordinates_lat())

        listing.coordinates = Point(lng, lat)

        street = None
        # Updating address
        if listing.street is None or need_update_address:
            address_dict = {
                'uk': self.fetch_geo_data(lng, lat, lang='uk'),
                'en': self.fetch_geo_data(lng, lat, lang='en')
                }

            if address_dict['uk'] and address_dict['en']:
                street = self.create_listing_address(address_dict)
                listing.street_number = address_dict['uk']['street']['num']
        if street:
            listing.street = street

        manager = self.get_manager(data.get('user', False))
        if manager:
            listing.manager = manager

        listing.save()

        
        # Create Images
        for image_url in data['images']:
            add_listing_image.delay(listing.id, image_url)

        # Update images
        for image in listing.images.all():
            if image.image_url not in data['images']:
                delete_listing_image.delay(image.id)

        # Clear all kits
        listing.kits.clear()
        # Create Kits (Attributes)
        for attribute_data in data['properties']:
            if attribute_data['id'] not in Attribute.BLACKLIST_ATTRIBUTES:
                # get or create attribute
                try:
                    attribute = Attribute.objects.get(slug=attribute_data['id'])
                except Attribute.DoesNotExist:
                    attribute = Attribute()
                    attribute.slug = attribute_data['id']
                    attribute.set_current_language('uk')
                    attribute.title = translate(attribute_data['label'], to_lang=languages['uk'])
                    attribute.set_current_language('en')
                    attribute.title = translate(attribute_data['label'], to_lang=languages['en'])
                    attribute.save()
                
                try:
                    kit = Kit.objects.get(attribute=attribute, untranslated_value=attribute_data['value'])
                except Kit.DoesNotExist:
                    kit = Kit()
                    kit.untranslated_value = attribute_data['value']
                    kit.set_current_language('uk')
                    kit.value = translate(attribute_data['value'], to_lang=languages['uk'])
                    kit.set_current_language('en')
                    kit.value = translate(attribute_data['value'], to_lang=languages['en'])
                    kit.attribute = attribute
                    kit.save()
                kit.listing.add(listing)
            elif attribute_data['id'] == 'property_71':
                try:
                    validate_url(attribute_data['value'])
                    listing.video_url = attribute_data['value']
                    listing.save()
                except ValidationError:
                    pass
    
    def create_listing_address(self, address_dict):
        try: 
            country = Country.objects.get(
                translations__language_code='uk',
                translations__title=address_dict['uk']['country']['title']
                )
        except Country.DoesNotExist:
            country = Country()
            country.set_current_language('uk')
            country.title = address_dict['uk']['country']['title']
            country.set_current_language('en')
            country.title = address_dict['en']['country']['title']
            country.save()
        
        if not country:
            return None
        
        try: 
            city = City.objects.get(
                translations__language_code='uk',
                translations__title=address_dict['uk']['city']['title']
                )
        except City.DoesNotExist:
            city = City()
            city.set_current_language('uk')
            city.title = address_dict['uk']['city']['title']
            city.set_current_language('en')
            city.title = address_dict['en']['city']['title']
            city.country = country
            city.save()
        
        if not city:
            return None
        
        try: 
            street = Street.objects.get(
                translations__language_code='uk',
                translations__title=address_dict['uk']['street']['title']
                )
        except Street.DoesNotExist:
            street = Street()
            street.set_current_language('uk')
            street.title = address_dict['uk']['street']['title']
            street.set_current_language('en')
            street.title = address_dict['en']['street']['title']
            street.city = city
            street.save()
        
        if not city:
            return None

        return street

    def get_category(self, category):
        if not category:
            return None
        
        try:
            term = Category.objects.get(
                translations__title=category, 
                translations__language_code='uk')
        except Category.DoesNotExist:
            term = Category()
            term.set_current_language('uk')
            term.title = category
            term.set_current_language('en')
            term.title = translate(category, to_lang=languages['en'])
            term.save()
        return term

    def get_realty_type(self, realty):
        if not realty:
            return None
        
        try:
            term = RealtyType.objects.get(
                translations__title=realty, 
                translations__language_code='uk')
        except RealtyType.DoesNotExist:
            term = RealtyType()
            term.set_current_language('uk')
            term.title = realty
            term.set_current_language('en')
            term.title = translate(realty, to_lang=languages['en'])
            term.save()
        return term

    def get_deal(self, deal):
        if deal:
            deal, _ = Deal.objects.get_or_create(slug=slugify(deal, allow_unicode=False), defaults={'title': deal})
            return deal
        return None
