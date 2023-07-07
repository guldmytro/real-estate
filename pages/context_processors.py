from .models import Contact


def contacts(request):
    try:
        contacts = Contact.objects.get()
    except:
        contacts = False
    return {'contacts': contacts}