from django.shortcuts import render
from .models import About, Abroad, Contact, Course
from managers.models import Review
from emails.forms import FeadbackForm
from django.core.paginator import Paginator, EmptyPage
from .forms import SearchManager, SellerForm
from emails.forms import ReviewForm
from django.urls import reverse_lazy
from listings.forms import SearchForm, SearchFormSimplified
from news.models import News


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
    crumbs = [
        ('Контакти', reverse_lazy('pages:contacts'))
    ]
    context = {
        'page': page,
        'feadback_form': feadback_form,
        'crumbs': crumbs
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


def pricing(request):
    feadback_form = FeadbackForm(request.POST)
    crumbs = [
        ('Вартість послуг', reverse_lazy('pages:pricing'))
    ]
    context = {
        'feadback_form': feadback_form,
        'crumbs': crumbs
    }
    return render(request, 'pages/pricing.html', context)


def reviews(request):
    search_manager_form = SearchManager()
    review_form = ReviewForm()
    reviews_list = Review.objects.select_related('manager').all()
    paginator = Paginator(reviews_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        reviews = paginator.page(page_number)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    context = {
        'reviews': reviews,
        'search_manager_form': search_manager_form,
        'review_form': review_form,
    }
    return render(request, 'pages/reviews.html', context)


def seller(request):
    seller_form = SellerForm(initial={'phone': '+380'})

    context = {
        'seller_form': seller_form
    }
    return render(request, 'pages/seller.html', context)


def guarantees(request):
    feadback_form = FeadbackForm(request.POST)
    reviews = Review.objects.select_related('manager').order_by('-rating')[:10]
    context = {
        'feadback_form': feadback_form,
        'reviews': reviews
    }
    return render(request, 'pages/guarantees.html', context)


def home(request):
    search_form = SearchForm(request.GET)
    search_form_simplified = SearchFormSimplified()
    feadback_form = FeadbackForm(request.POST)
    news = News.objects.order_by('-created')[:10]
    reviews = Review.objects.select_related('manager').order_by('-rating')[:10]
    context = {
        'search_form': search_form,
        'search_form_simplified': search_form_simplified,
        'feadback_form': feadback_form,
        'news': news,
        'reviews': reviews
    }
    return render(request, 'pages/home.html', context)
