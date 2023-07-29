from celery import shared_task
from listings.models import Image, Listing

@shared_task
def add_listing_image(listing_id, image_url):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        pass
    if listing:
        try:
            image = Image.objects.get(image_url=image_url, listing=listing)
        except Image.DoesNotExist:
            image = Image(image_url=image_url, listing=listing)
            try:
                image.full_clean()
                image.save()
            except:
                pass


@shared_task
def delete_listing_image(image_id):
    try:
        Image.objects.get(id=image_id).delete()
    except:
        pass
