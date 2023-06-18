from .forms import FILTER_PROPS

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