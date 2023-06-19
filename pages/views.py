from django.shortcuts import render
from .models import About, Abroad
from managers.models import Review
from emails.forms import FeadbackForm


def about(request):
    feadback_form = FeadbackForm(request.POST)
    page = About.objects.prefetch_related('items').get()
    reviews = Review.objects.select_related('manager').order_by('-rating')[:10]
    context = {
        'page': page,
        'reviews': reviews,
        'feadback_form': feadback_form
    }
    return render(request, 'pages/about.html', context)


def abroad_properties(request):
    feadback_form = FeadbackForm(request.POST)
    page = Abroad.objects.prefetch_related('items').get()
    context = {
        'page': page,
        'feadback_form': feadback_form
    }
    return render(request, 'pages/abroad.html', context)
