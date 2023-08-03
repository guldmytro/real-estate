from django.utils.translation import activate

class NewUserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('visited'):
            request.session['visited'] = True
            activate('uk')
        
        response = self.get_response(request)
        return response