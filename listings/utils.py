from .models import Listing, Kit, City, Street


def filter_listings(cleaned_data, listings):
    city_id = cleaned_data.get('city')
    street_id = cleaned_data.get('street')
    number_of_rooms = cleaned_data.get('number_of_rooms')
    min_price = cleaned_data.get('min_price')
    max_price = cleaned_data.get('max_price')
    realty_type = cleaned_data.get('realty_type')

    repair = cleaned_data.get('repair')
    lift = cleaned_data.get('lift')
    parking = cleaned_data.get('parking')
    outside_decorating = cleaned_data.get('outside_decorating')
    floor_from = cleaned_data.get('floor_from')
    floor_to = cleaned_data.get('floor_to')
    floors_from = cleaned_data.get('floors_from')
    floors_to = cleaned_data.get('floors_to')

    if street_id:
        listings = listings.filter(street_id=street_id)
    elif city_id:
        listings = listings.filter(street__city_id=city_id)
    
    if number_of_rooms:
        if number_of_rooms == '4+':
            listings = listings.filter(room_count__gte=4)
        else:
            listings = listings.filter(room_count=number_of_rooms)

    if min_price and max_price:
        listings = listings.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        listings = listings.filter(price__gte=min_price)
    elif max_price:
        listings = listings.filter(price__lte=max_price)

    if realty_type:
        listings = listings.filter(realty_type=realty_type)

    if repair:
        listings = listings.filter(kits=repair)

    if lift:
        listings = listings.filter(kits=lift)

    if parking:
        listings = listings.filter(kits=parking)

    if outside_decorating:
        listings = listings.filter(kits=outside_decorating)

    if floor_from:
        listings = listings.filter(floor__gte=floor_from)
        
    if floor_to:
        listings = listings.filter(floor__lte=floor_to)

    if floors_from:
        listings = listings.filter(total_floors__gte=floors_from)

    if floors_to:
        listings = listings.filter(total_floors__lte=floors_to)
        
    return listings


def get_similar_listings(listing):
    city = listing.street.city
    room_count = listing.room_count

    similar_listings = Listing.active.filter(
        street__city=city,
        room_count=room_count,
    ).exclude(id=listing.id)


    try: 
        kit = Kit.objects.get(attribute__slug='property_23', listing=listing)
        year_built = int(kit.value)

        min_year_built = year_built - 3
        max_year_built = year_built + 3

        similar_listings = similar_listings.filter(
            kits__attribute__slug='property_23',
            kits__value__gte=str(min_year_built),
            kits__value__lte=str(max_year_built),
        )
    except Kit.DoesNotExist:
        pass

    similar_listings = similar_listings[:10]

    return similar_listings


def modify_get(GET):
    modified_get = GET.copy()
    city = modified_get.get('city')
    street = modified_get.get('street')
    try:
        if city:
            city_obj = City.objects.get(id=city)
            modified_get['address_input'] = city_obj.title
        elif street:
            street_obj = Street.objects.get(id=street)
            modified_get['address_input'] = f'{street_obj.title} ({street_obj.city.title})'
    except:
        pass
    return modified_get