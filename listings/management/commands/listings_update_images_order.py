from django.core.management.base import BaseCommand
from props.models import SiteConfiguration, Feed
import requests
import xml.etree.ElementTree as ET
from listings.models import Listing, Image
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
    help = 'Update listings images order from feed API'

    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        logger.info('Started listings update currency')
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
            if child.tag == 'images':
                images = []
                for image_url in child.iter('image_url'):
                    images.append(self.clear_string(image_url.text))
                item_dict[child.tag] = images
        return item_dict

    
    def update_models(self):
        logger.info(f'Total items from CRM - {len(self.items)} item(s)')
        for item in self.items:
            id = item.get('id')
            if id is None:
                continue
            try:
                listing = Listing.objects.get(id=int(id))
                for index, src in enumerate(item['images']):
                    try:
                        current_image = listing.images.get(image_url=src)
                        current_image.order = index
                        current_image.save()
                        print(f'update for {listing.id}')
                    except Image.DoesNotExist:
                        print(f'Image doesnt exist for {listing.id} and src {src}')
                listing.save()
                logger.info(f'Successfully updated image ordering for listing {listing.id}')
            except Listing.DoesNotExist:
                logger.error(f'Listing {id} does not exist')

    def clear_string(self, str):
        if str is not None:
            return strip_tags(re.sub(r'^\s+|\s+$|\s+(?=\s)', '', str))
        return str


