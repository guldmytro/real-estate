def filter_listings(cleaned_data, listings):
    city_id = cleaned_data.get('city')
    street_id = cleaned_data.get('street')
    number_of_rooms = cleaned_data.get('number_of_rooms')
    min_price = cleaned_data.get('min_price')
    max_price = cleaned_data.get('max_price')
    realty_type_id = cleaned_data.get('realty_type')

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

    if realty_type_id:
        listings = listings.filter(realty_type_id=realty_type_id)
        
    return listings