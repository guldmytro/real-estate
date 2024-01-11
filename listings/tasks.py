from celery import shared_task
from listings.models import Image, Listing, Manager

@shared_task
def add_listing_image(listing_id, image_url, index):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        pass
    if listing:
        try:
            image = Image.objects.get(image_url=image_url, listing=listing)
        except Image.DoesNotExist:
            image = Image(image_url=image_url, order=index, listing=listing)
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


@shared_task
def add_manager_image(manager_id, image_url):
    try:
        manager = Manager.objects.get(id=manager_id)
    except Manager.DoesNotExist:
        pass

    if manager.image is None or image_url != manager.image_url:
        try:
            manager.image_url = image_url
            manager.save()
        except:
            pass