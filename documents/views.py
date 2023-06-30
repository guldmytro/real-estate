from django.shortcuts import render
from .models import Document
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse_lazy


def documents_list(request):
    document_list = Document.objects.all()
    paginator = Paginator(document_list, 10)
    page_number = request.GET.get('page', 1)
    try:
        documents = paginator.page(page_number)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    crumbs = [
        ('Документи', reverse_lazy('documents:list'))
    ]
    context = {
        'documents': documents,
        'crumbs': crumbs
    }
    return render(request, 'documents/list.html', context)
