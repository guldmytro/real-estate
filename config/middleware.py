from django.utils.translation import activate
from django.shortcuts import redirect
from listings.models import City
from django.db.models import Count

class NewUserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('visited'):
            request.session['visited'] = True
            activate('ru')
        
        response = self.get_response(request)
        return response
    

class NewUserCityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('current_city'):
            cities_qs = City.objects.annotate(cnt=Count('streets__listings'))\
                .filter(cnt__gte=1,
                        translations__language_code=request.LANGUAGE_CODE)\
                .order_by('-cnt')
            city = cities_qs.first()
            request.session['current_city'] = city.pk
        response = self.get_response(request)
        return response