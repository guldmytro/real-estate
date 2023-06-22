from django.shortcuts import render
from .models import About, Abroad, Contact, Course
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


def contacts(request):
    feadback_form = FeadbackForm(request.POST)
    page = Contact.objects.get()
    context = {
        'page': page,
        'feadback_form': feadback_form
    }
    return render(request, 'pages/contacts.html', context)


def course(request):
    feadback_form = FeadbackForm(request.POST)
    page = Course.objects.get()
    context = {
        'page': page,
        'feadback_form': feadback_form
    }
    return render(request, 'pages/course.html', context)