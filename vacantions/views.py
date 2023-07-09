from django.shortcuts import render
from .models import Vacantion
from django.core.paginator import Paginator, EmptyPage
from emails.forms import ApplyForm, FeadbackForm
from pages.models import VacantionPage
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def vacantions_list(request):
    crumbs = [
        (_('Vacancies'), reverse_lazy('vacantions:page')),
        (_('List'), reverse_lazy('vacantions:list')),
    ]
    apply_form = ApplyForm()
    vacantions_list = Vacantion.objects.all()
    count = vacantions_list.count()
    paginator = Paginator(vacantions_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        vacantions = paginator.page(page_number)
    except EmptyPage:
        vacantions = paginator.page(paginator.num_pages)
    context = {
        'vacantions': vacantions,
        'count': count,
        'apply_form': apply_form,
        'crumbs': crumbs
    }
    return render(request, 'vacantions/list.html', context)


def vacantions_page(request):
    feadback_form = FeadbackForm()
    page = VacantionPage.objects.get()
    context = {
        'page': page,
        'feadback_form': feadback_form
    }
    return render(request, 'vacantions/page.html', context)
