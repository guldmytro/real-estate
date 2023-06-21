from django.shortcuts import render
from .models import Vacantion
from django.core.paginator import Paginator, EmptyPage
from emails.forms import ApplyForm


def vacantions_list(request):
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
        'apply_form': apply_form
    }
    return render(request, 'vacantions/list.html', context)
