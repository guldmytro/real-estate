from celery import shared_task
from listings.models import Image, Listing, Manager

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


@shared_task
def add_manager_image(manager_id, image_url):
    print(f'running add manager_image with {manager_id} and {image_url}')
    try:
        manager = Manager.objects.get(id=manager_id)
    except Manager.DoesNotExist:
        print('Manager Does Not exist')
        pass

    if manager.image is None or image_url != manager.image_url:
        print('image of existing manager is None or image_url not the same as manager.image_url')
        try:
            manager.image_url = image_url
            manager.save()
        except:
            print('Error while trying to save manager')
            pass
    print('other')