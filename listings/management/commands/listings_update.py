from django.core.management.base import BaseCommand
from props.models import SiteConfiguration
import requests
import xml.etree.ElementTree as ET
import json
import re
from django.utils.html import strip_tags
from listings.models import Listing, Category, RealtyType, Image, Kit, Attribute
from django.contrib.gis.geos import Point
from django.utils.text import slugify


config = SiteConfiguration.objects.get()
CRM_API = config.crm_api


class Command(BaseCommand):
    help = 'Update listings from Feed API'

    def handle(self, *args, **options):
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
            listing.coordinates = Point(float(data['location']['map_lng']), float(data['location']['map_lat']))

            listing.save()

            # Create Images
            for image_url in data['images']:
                image = Image(image_url=image_url, listing=listing)
                try:
                    image.full_clean()
                    image.save()
                except:
                    pass

            # Create Kits (Attributes)
            for attribute_data in data['properties']:
                attribute, _ = Attribute.objects.get_or_create(title=attribute_data['label'], slug=attribute_data['id'])
                Kit.objects.create(listing=listing, attribute=attribute, value=attribute_data['value'])


