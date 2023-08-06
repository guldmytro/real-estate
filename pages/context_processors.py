from .models import Contact
from django.conf import settings

def contacts(request):
    try:
        contacts = Contact.objects.get()
    except:
        contacts = False
    return {'contacts': contacts}


def static_version(request):
    return {'ver': settings.STATIC_VERSION}