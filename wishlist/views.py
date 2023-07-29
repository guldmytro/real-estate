from django.shortcuts import render
from listings.models import Listing
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


def wishlist_archive(request):
    ids = list(filter(lambda id: id != '', request.COOKIES.get('wishlist', '').split(',')))
    listings_list = Listing.objects.prefetch_related('images').filter(id__in=ids)
    paginator = Paginator(listings_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        listings = paginator.page(page_number)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)
    context = {
        'listings': listings
    }
    return render(request, 'wishlist/list.html', context)


@require_POST
def wishlist_count(request):
    try:
        body = json.loads(request.body)
        wishlist = body.get('wishlist')
        ids = list(filter(lambda id: id != '', wishlist.split(',')))
        cnt = Listing.objects.filter(id__in=ids).count()
        if cnt > 9:
            cnt = '9+'
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except:
        return JsonResponse({'error': 'Server error'}, status=500)
    return JsonResponse({'cnt': cnt})
