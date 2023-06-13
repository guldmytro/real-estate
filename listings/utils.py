def filter_listings(request, listings):
    city_id = request.GET.get('city')
    street_id = request.GET.get('street')
    if street_id:
        listings = listings.filter(street_id=street_id)
    elif city_id:
        listings = listings.filter(street__city_id=city_id)
    return listings