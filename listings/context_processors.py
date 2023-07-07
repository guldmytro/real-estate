from .models import RealtyType, Listing
from django.db.models import Count


def real_types(request):
    real_types = RealtyType.objects.annotate(cnt=Count('listings'))\
        .filter(cnt__gt=0).exclude(menu_label__isnull=True)\
        .order_by('menu_label')
    return {'real_types': real_types}


def wishlist_types(request):
    ids = list(filter(lambda id: id != '', request.COOKIES.get('wishlist', '').split(',')))
    wishlist_count = Listing.objects.filter(id__in=ids).count()
    if wishlist_count > 9:
        wishlist_count = '9+'
    return {'wishlist_count': wishlist_count}