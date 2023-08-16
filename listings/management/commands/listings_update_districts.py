from django.core.management.base import BaseCommand
from props.models import SiteConfiguration, Feed
import requests
import xml.etree.ElementTree as ET
from listings.models import Listing, District, HouseComplex
import re
from django.utils.html import strip_tags
from listings.utils import translate


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('cron.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)




config = SiteConfiguration.objects.get()
GOOGLE_API_KEY = config.google_api_key


class Command(BaseCommand):
    help = 'Update listings districts from feed API'

    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        logger.info('Started listings update districts')
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

            self.update_models()


    def parse_item(self, item):
        item_dict = {
            'id': item.get('internal-id'),
        }
        for child in item:
            if child.tag == 'location':
                location = {}
                for location_child in child:
                    if location_child.tag == 'metros':
                        metros = []
                        for metro in location_child:
                            if metro.tag == 'metro':
                                metros.append({
                                    'name': self.clear_string(metro.text),
                                    'distance': int(metro.get('value'))
                                })
                        location[location_child.tag] = metros
                    else: location[location_child.tag] = self.clear_string(location_child.text)
                item_dict[child.tag] = location
            elif child.tag == 'newbuilding_name':
                item_dict[child.tag] = self.clear_string(child.text)
        return item_dict

    
    def update_models(self):
        logger.info(f'Total items from CRM - {len(self.items)} item(s)')
        for item in self.items:
            id = item.get('id')
            if id is None:
                continue
            try:
                listing = Listing.objects.get(id=int(id))
                listing.district = self.get_listing_district(item['location'].get('district'), listing.street)
                listing.house_complex = self.get_listing_house_complex(item.get('newbuilding_name'), listing.street)
                listing.set_current_language('uk')
                listing.metros = self.get_formatted_metros(item['location'].get('metros'))
                listing.set_current_language('en')
                listing.metros = translate(self.get_formatted_metros(item['location'].get('metros')))
                listing.save()
                logger.info(f'Successfully updated district and house complex for listing {listing.id}')
            except Listing.DoesNotExist:
                logger.error(f'Listing {id} does not exist')


    def get_listing_district(self, district, street):
        if street is None or district is None:
            return None
        if street.city is None:
            return None
        
        city = street.city
        district_obj = None

        try: 
            district_obj = District.objects.get(
                translations__language_code='uk',
                translations__title=district
                )
        except District.DoesNotExist:
            district_obj = District()
            district_obj.set_current_language('uk')
            district_obj.title = district
            district_obj.set_current_language('en')
            district_obj.title = translate(district, from_lang='uk', to_lang='en')
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
                translations__title=house_complex
                )
        except HouseComplex.DoesNotExist:
            house_complex_obj = HouseComplex()
            house_complex_obj.set_current_language('uk')
            house_complex_obj.title = house_complex
            house_complex_obj.set_current_language('en')
            house_complex_obj.title = translate(house_complex, from_lang='uk', to_lang='en')
            house_complex_obj.city = city
            house_complex_obj.save()

        return house_complex_obj


    def clear_string(self, str):
        if str is not None:
            return strip_tags(re.sub(r'^\s+|\s+$|\s+(?=\s)', '', str))
        return str
    
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


