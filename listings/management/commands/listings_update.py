from django.core.management.base import BaseCommand, CommandParser
from props.models import SiteConfiguration, Feed
import requests
import xml.etree.ElementTree as ET
import json
import re
from django.utils.html import strip_tags
from listings.models import Listing, Category, RealtyType, Deal, \
    Kit, Attribute, Country, City, Street, Region, District, HouseComplex, Image
from managers.models import Manager, Phone
from django.contrib.gis.geos import Point
from slugify import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from listings.utils import translate, languages
from listings.tasks import add_listing_image, delete_listing_image, add_manager_image
from django.core.exceptions import ValidationError
from listings.utils import convert_to_utc
from django.utils import timezone
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('cron.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

validate_url = URLValidator()


config = SiteConfiguration.objects.get()
GOOGLE_API_KEY = config.google_api_key


class Command(BaseCommand):
    help = 'Update listings from Feed API'

    def add_arguments(self, parser):
        parser.add_argument('--update_date', dest='update_date', type=str)
        parser.add_argument('--all', dest='all', type=str)

    def handle(self, *args, **options):
        self.update_date = options.get('update_date', '').lower() == 'yes' if options.get('update_date') is not None else False
        self.all = options.get('all', '').lower() == 'all' if options.get('all') is not None else False
        feeds = Feed.objects.all()
        logger.info('Started listings update')
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

            self.items = []
            for item in root:
                self.items.append(self.parse_item(item))

            logger.info(f'Total items from CRM - {len(self.items)} item(s)')
            today_utc = datetime.now(pytz.UTC).replace(hour=0, minute=0, second=0, microsecond=0)
            self.filtered_items = [
                item for item in self.items
                if ("created_at" in item and convert_to_utc(item["created_at"]).date() == today_utc.date()) or
                   ("updated_at" in item and convert_to_utc(item["updated_at"]).date() == today_utc.date())
            ]
            logger.info(f'Items for updating - {len(self.filtered_items)} item(s)')
            self.update_models()

    def handle_d(self, *args, **options):
        with open('api-result.json', encoding='utf-8') as json_file:
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
                    if location_child.tag == 'metros':
                        metros = []
                        metro_names = []
                        for metro in location_child:
                            if metro.tag == 'metro':
                                if self.clear_string(metro.text) not in metro_names:
                                    metros.append({
                                        'name': self.clear_string(metro.text),
                                        'distance': int(metro.get('value'))
                                    })
                                    metro_names.append(self.clear_string(metro.text))
                        location[location_child.tag] = metros
                    else:
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
            elif child.tag == 'price':
                item_dict[child.tag] = self.clear_string(child.text)
                item_dict['currency'] = self.clear_string(child.get('currency'))
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

        # Extract region
        region = next(
            (component for component in response_json['results'][0]['address_components'] if
             'administrative_area_level_1' in component['types']),
            None
        )
        region_title = region['long_name'] if region else None 

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
        if street is not None:
            street_title = street['long_name'] if street else None
        else:
            street = next(
                (component for component in response_json['results'] if
                'route' in component['types']),
                None
            )
            try:
                street_deep = next(
                    (component for component in street['address_components'] if
                     'route' in component['types']),
                     None
                )
                street_title = street_deep['long_name'] if street else None  
            except:
                street_title = None
        

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
            'region': {
                'title': region_title,
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
            manager.set_current_language('uk')
            if manager.full_name != name:
                print('old name ', manager.full_name)
                print('new name ', name)
                manager.full_name = name
                manager.set_current_language('en')
                manager.full_name = name
                manager.save()
            
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
        
        # Updating Image (if it needs)
        image_url = user.get('image_url', False)
        if image_url:
            add_manager_image.delay(manager.id, image_url)

        
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

 
        
        return manager

    def update_models(self):
        items = self.filtered_items
        if self.update_date or self.all:
            items = self.items

        for data in items:
            try: 
                if self.update_date:
                    logger.info(f'Updating datetimefield for listing {data["id"]}')
                    self.listings_update_date(data)
                elif data['status'] != 'active':
                    logger.info(f'Deleting listing {data["id"]}')
                    self.delete_listing(data)
                else:
                    self.add_listing(data)
                    logger.info(f'Updating listing {data["id"]}')
            except Exception as e: 
                logger.error(f'Error while working with listing {data["id"]}: {str(e)}')
                pass
        logger.info('Finished listings_update')

    def listings_update_date(self, data):
        try:
            listing = Listing.objects.get(id=int(data['id']))
            listing.created = convert_to_utc(data.get('created_at', timezone.now()))
            listing.updated = convert_to_utc(data.get('updated_at', timezone.now()))
            listing.save()
        except Listing.DoesNotExist:
            pass

    def add_listing(self, data):
        # Create or update Category and RealtyType
        category = self.get_category(data.get('category', False))
        realty_type = self.get_realty_type(data.get('realty_type', False))
        deal = self.get_deal(data.get('deal', False))

        # get or create listing
        print(int(data['id']))
        try:
            listing = Listing.objects.get(id=int(data['id']))
            if listing.created == convert_to_utc(data.get('created_at', timezone.now())) and \
               listing.updated == convert_to_utc(data.get('updated_at', timezone.now())):
                logger.info(f'Listing {data["id"]} is already updated')
                return False
        except Listing.DoesNotExist:
            listing = Listing(id=int(data['id']))
        listing.status = 'active'
        listing.created = convert_to_utc(data.get('created_at', timezone.now()))
        listing.updated = convert_to_utc(data.get('updated_at', timezone.now()))
        same_title = False
        same_description = False
        listing.set_current_language('uk')
        try:
            same_title = listing.title == data['title']
        except:
            pass
        try:
            same_description = listing.description == data['description']
        except:
            pass
        listing.title = data['title']
        listing.description = data.get('description', '')
        listing.set_current_language('en')
        if not same_title:
            listing.title = translate(data['title'], from_lang=languages['uk'], to_lang=languages['en'])
        if not same_description:
            listing.description = translate(data.get('description', ''), to_lang=['en'])

        listing.set_current_language('uk')
        listing.metros = self.get_formatted_metros(data['location'].get('metros'))
        listing.set_current_language('en')
        listing.metros = translate(self.get_formatted_metros(data['location'].get('metros')))

        listing.is_new_building = bool(int(data.get('is_new_building', '0')))
        
        listing.area_total = int(round(float(data.get('area_total', '0'))))
        listing.area_living = int(round(float(data.get('area_living', '0'))))
        listing.area_kitchen = int(round(float(data.get('area_kitchen', '0'))))
        listing.room_count = int(data.get('room_count', '0'))
        listing.floor = int(data.get('floor', '0'))
        listing.total_floors = int(data.get('total_floors', '0'))
        listing.price = int(data.get('price', '0'))
        api_currency = data.get('currency')
        if api_currency == 'UAH':
            listing.currency = '₴'
        elif api_currency == 'USD':
            listing.currency = '$'
        listing.category = category
        listing.realty_type = realty_type
        listing.deal = deal

        lng = float(data['location']['map_lng'])
        lat = float(data['location']['map_lat'])
        
        listing.coordinates = Point(lng, lat)

        street = None
        # Updating address
        # address_dict = {
        #     'uk': self.fetch_geo_data(lng, lat, lang='uk'),
        #     'en': self.fetch_geo_data(lng, lat, lang='en')
        #     }
        # if address_dict['uk'] and address_dict['en']:
        street = self.create_listing_address(data.get('location', {}))
        try:
            listing.street_number = data['location'].get('house_num', '')
        except:
            pass
                    
        if street:
            listing.street = street
        
        listing.district = self.get_listing_district(data['location'].get('district'), listing.street, data['location'].get('district_ru'))
        listing.house_complex = self.get_listing_house_complex(data.get('newbuilding_name'), listing.street)

        manager = self.get_manager(data.get('user', False))
        if manager:
            listing.manager = manager
        try:
            listing.full_clean()
            listing.save()
        except ValidationError as e:
            print(f'Error while trying to save {int(data["id"])}. Error: {e}')
            return False

        
        # Create Images
        for index, image_url in enumerate(data['images']):
            # add_listing_image.delay(listing.id, image_url, index)
            try:
                image = Image.objects.get(image_url=image_url, listing=listing)
            except Image.DoesNotExist:
                image = Image(image_url=image_url, order=index, listing=listing)
                try:
                    image.full_clean()
                    image.save()
                except:
                    pass

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
                    attribute.set_current_language('ru')
                    attribute.title = translate(attribute_data['label'], to_lang=languages['ru'])
                    attribute.save()
                
                try:
                    kit = Kit.objects.get(attribute=attribute, untranslated_value=attribute_data['value'])
                except Kit.DoesNotExist:
                    kit = Kit()
                    kit.untranslated_value = attribute_data['value']

                    if str(attribute_data['value']).lower() == 'есть':
                        kit.set_current_language('uk')
                        kit.value = 'Є'
                        kit.set_current_language('en')
                        kit.value = 'There is gas'
                        kit.set_current_language('ru')
                        kit.value = 'Есть'
                    elif str(attribute_data['value']).lower() == 'евроремонт':
                        kit.set_current_language('uk')
                        kit.value = 'Євроремонт'
                        kit.set_current_language('en')
                        kit.value = 'Renovation'
                        kit.set_current_language('ru')
                        kit.value = 'Евроремонт'
                    else:
                        kit.set_current_language('uk')
                        kit.value = translate(attribute_data['value'], to_lang=languages['uk'])
                        kit.set_current_language('en')
                        kit.value = translate(attribute_data['value'], to_lang=languages['en'])
                        kit.set_current_language('ru')
                        kit.value = translate(attribute_data['value'], to_lang=languages['ru'])
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
    
    def delete_listing(self, data):
        try:
            listing = Listing.objects.get(id=int(data['id']))
            listing.delete()
            logger.info(f'Listing {int(data["id"])} deleted')
        except Listing.DoesNotExist:
            logger.error(f'Listing {int(data["id"])} does not exist')

    
    def create_listing_address(self, location):
        country_t = location.get('country', None)
        country_t_ru = location.get('country', None)
        region_t = location.get('region', None)
        region_t_ru = location.get('region', None)
        city_t = location.get('city', None)
        city_t_ru = location.get('city_ru', None)
        street_t = location.get('street', None)
        street_t_ru = location.get('street_ru', None)

        if country_t is None:
            return None
        try: 
            country = Country.objects.get(
                translations__language_code='uk',
                translations__title=country_t
                )
        except Country.DoesNotExist:
            country = Country()
            country.set_current_language('uk')
            country.title = country_t
            country.set_current_language('en')
            country.title = country_t
            country.set_current_language('ru')
            country.title = country_t_ru
            country.save()
        
        if not country:
            return None
        
        if region_t is None:
            return None
        
        region = None
        try:
            region = Region.objects.get(
                translations__language_code='uk',
                translations__title=region_t
            )
        except Region.DoesNotExist:
            region = Region()
            region.set_current_language('uk')
            region.title = region_t
            region.set_current_language('en')
            region.title = region_t
            region.set_current_language('ru')
            region.title = region_t_ru
            region.save()
        
        if city_t is None:
            return None
        
        try: 
            city = City.objects.get(
                translations__language_code='uk',
                translations__title=city_t,
                region=region
                )
        except City.DoesNotExist:
            city = City()
            city.set_current_language('uk')
            city.title = city_t
            city.set_current_language('en')
            city.title = city_t
            city.set_current_language('ru')
            city.title = city_t_ru
            city.country = country
            if region:
                city.region = region
            city.save()
        
        if not city:
            return None
        
        if street_t is None:
            return None
        try: 
            street = Street.objects.get(
                translations__language_code='uk',
                translations__title=street_t,
                city=city
                )
        except Street.DoesNotExist:
            street = Street()
            street.set_current_language('uk')
            street.title = street_t
            street.set_current_language('en')
            street.title = street_t
            street.set_current_language('ru')
            street.title = street_t_ru
            street.city = city
            street.save()

        
        if not city:
            return None

        return street
    
    def get_listing_district(self, district, street, district_ru):
        if street is None or district is None:
            return None
        if street.city is None:
            return None
        
        city = street.city
        district_obj = None

        try: 
            district_obj = District.objects.get(
                translations__language_code='uk',
                translations__title=district,
                city=city
                )
        except District.DoesNotExist:
            district_obj = District()
            district_obj.set_current_language('uk')
            district_obj.title = district
            district_obj.set_current_language('en')
            district_obj.title = translate(district, from_lang='uk', to_lang='en')
            district_obj.city = city
            district_obj.set_current_language('ru')
            district_obj.title = district_ru
            district_obj.city = city
            district_obj.save()

        return district_obj
    
    def get_listing_house_complex(self, house_complex, street):
        if street is None or house_complex is None:
            return None
        if street.city is None:
            return None
        
        city = street.city
        house_complex_obj = None

        try: 
            house_complex_obj = HouseComplex.objects.get(
                translations__language_code='uk',
                translations__title=house_complex,
                city=city
                )
        except HouseComplex.DoesNotExist:
            house_complex_obj = HouseComplex()
            house_complex_obj.set_current_language('uk')
            house_complex_obj.title = house_complex
            house_complex_obj.set_current_language('en')
            house_complex_obj.title = translate(house_complex, from_lang='uk', to_lang='en')
            house_complex_obj.city = city
            house_complex_obj.set_current_language('ru')
            house_complex_obj.title = translate(house_complex, from_lang='uk', to_lang='ru')
            house_complex_obj.city = city
            house_complex_obj.save()

        return house_complex_obj

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
            term.set_current_language('ru')
            term.title = translate(category, to_lang=languages['ru'])
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
            term.set_current_language('ru')
            term.title = translate(realty, to_lang=languages['ru'])
            term.save()
        return term

    def get_deal(self, deal):
        if deal:
            deal, _ = Deal.objects.get_or_create(slug=slugify(deal, allow_unicode=False), defaults={'title': deal})
            return deal
        return None
    

    def get_formatted_metros(self, metros):
        if metros == '' or metros is None:
            return ''
        formatted_strings = []
        for metro in sorted(metros, key=lambda x: x['distance']):
            distance_f = self.format_distance(metro['distance'])
            if distance_f is None:
                continue
            formatted_string = f"{metro['name']} ({distance_f})\n"
            formatted_strings.append(formatted_string)
        return "".join(formatted_strings).rstrip("\n")
    

    def format_distance(self, distance):
        dist = 0
        try: 
            dist = int(distance)
            if dist < 100:
                return f'{dist}м'
            rounded_dist = round(dist/1000, 1)
            return f'{rounded_dist}км'
        except:
            return None
