from django.shortcuts import render


def listings_list(request):
    return render(request, 'listings/list.html', {})
