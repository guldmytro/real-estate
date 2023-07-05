from .models import RealtyType
from django.db.models import Count


def real_types(request):
    real_types = RealtyType.objects.annotate(cnt=Count('listings'))\
        .filter(cnt__gt=0).exclude(menu_label__isnull=True)\
        .order_by('menu_label')
    return {'real_types': real_types}