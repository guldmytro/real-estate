from django.core.management.base import BaseCommand
from props.models import SiteConfiguration, Feed
import requests
import xml.etree.ElementTree as ET
from listings.models import Listing


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
    help = 'Delete listings from Feed API'

    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        logger.info('Started listings delete')
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
            if child.tag == 'status':
                item_dict[child.tag] = child.text
        return item_dict

    
    def update_models(self):
        ids = [int(item.get('id')) for item in self.items]
        closed_ids = [int(item.get('id')) for item in self.items if item.get('status') != 'active']
        try: 
            cnt, _ = Listing.objects.exclude(id__in=ids).delete()
            logger.info(f'Successfuly deleted {cnt} item(s)')
        except Exception as e:
            logger.error(f'Error while trying to delete listings - {e}')
        
        try: 
            cnt, _ = Listing.objects.filter(id__in=closed_ids).delete()
            logger.info(f'Successfuly deleted {cnt} item(s)')
        except Exception as e:
            logger.error(f'Error while trying to delete listings - {e}')


