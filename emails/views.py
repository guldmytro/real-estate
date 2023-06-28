from django.http import JsonResponse
from props.models import SiteConfiguration
from .forms import FeadbackForm, ApplyForm, ReviewForm,\
     ListingMessageForm, ListingPhoneForm, ListingVisitForm
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMultiAlternatives
from managers.models import Manager
from django.core.validators import validate_email
from django import forms
from django.shortcuts import get_object_or_404
from pages.forms import SellerForm
from listings.models import Listing


@require_POST
def feadback(request):
    form = FeadbackForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        config = SiteConfiguration.objects.get()
    
        context = {
            'name': cd['name'],
            'phone': cd['phone']
        }
        message = render_to_string('emails/feadback.html', context)
        to = config.email
        subject = 'Заявка на консультацію'
        sent = send_mail(subject, '', '', [to], html_message=message)
        if sent == 1:
            return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'bad'})


@require_POST
def apply(request):
    form = ApplyForm(request.POST, request.FILES)
    if form.is_valid():
        cd = form.cleaned_data
        config = SiteConfiguration.objects.get()

        context = {
            'name': cd['name'],
            'phone': cd['phone']
        }
        message = render_to_string('emails/feadback.html', context)
        to = config.email
        subject = 'Відгук на вакансію'
        email = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email='',
            to=[to],
        )

        # Attach the uploaded file dynamically
        for file_name, file_content in request.FILES.items():
            email.attach(file_name, file_content.read(), file_content.content_type)

        email.attach_alternative(message, 'text/html')

        try:
            email.send()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return JsonResponse({'status': 'bad'})
    else:
        return JsonResponse({'formErrors': form.errors})


@require_POST
def manager_quick_message(request, id):
    try:
        manager = Manager.objects.get(pk=id)
        form = FeadbackForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            config = SiteConfiguration.objects.get()
        
            context = {
                'manager': manager,
                'name': cd['name'],
                'phone': cd['phone']
            }
            message = render_to_string('emails/feadback-manager.html', context)
            
            try:
                validate_email(manager.email)
                to = [config.email, manager.email]
            except forms.ValidationError:
                to = [config.email]
            
            subject = 'Клієнт чекає зворотнього дзвінка'
            sent = send_mail(subject, '', '', to, html_message=message)
            if sent == 1:
                return JsonResponse({'status': 'ok'})
        
        return JsonResponse({'status': 'bad'})

    except Manager.DoesNotExist:
        return JsonResponse({'status': 'bad'})
    

@require_POST
def manager_add_review(request, id):
    review_form = ReviewForm(request.POST)
    manager = get_object_or_404(Manager, id=id)
    if review_form.is_valid():
        cd = review_form.cleaned_data
        review_form.save()
        config = SiteConfiguration.objects.get()
        context = {
            'manager': manager,
            'name': cd['author'],
            'phone': cd['phone'],
            'rating': cd['rating'],
            'body': cd['body']
        }
        message = render_to_string('emails/review-manager.html', context)
        
        try:
            validate_email(manager.email)
            to = [config.email, manager.email]
        except forms.ValidationError:
            to = [config.email]
        
        subject = 'Відвідувач сайту залишив відгук'
        send_mail(subject, '', '', to, html_message=message)
        
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'formErrors': review_form.errors})
    

@require_POST
def seller_quick_message(request):
    seller_form = SellerForm(request.POST)
    if seller_form.is_valid():
        cd = seller_form.cleaned_data
        context = {
            'phone': cd['phone'],
            'type': cd['realty_type']
        }
        config = SiteConfiguration.objects.get()
        message = render_to_string('emails/feadback-seller.html', context)
        to = config.email
        subject = 'Заявка на консультацію'
        sent = send_mail(subject, '', '', [to], html_message=message)
        if sent == 1:
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'ok'})    
    return JsonResponse({'status': 'bad'})


@require_POST
def listing_quick_message(request, id):
    try:
        listing = Listing.objects.select_related('manager').get(id=id)
        form = ListingPhoneForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            config = SiteConfiguration.objects.get()
        
            context = {
                'listing': listing,
                'phone': cd['phone'],
            }
            message = render_to_string('emails/listing_phone.html', context)
            to = [config.email]
            if listing.manager:
                to.append(listing.manager.email)

            subject = 'Нове повідомлення з сайту'
            sent = send_mail(subject, '', '', [to], html_message=message)
            if sent == 1:
                return JsonResponse({'status': 'ok'})

    except Listing.DoesNotExist:
        return JsonResponse({'status': 'bad', 'message': 'listing is not found'})
    return JsonResponse({'status': 'bad', 'message': 'bad response'})


@require_POST
def listing_message(request, id):
    try:
        listing = Listing.objects.select_related('manager').get(id=id)
        form = ListingMessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            config = SiteConfiguration.objects.get()
        
            context = {
                'listing': listing,
                'phone': cd['phone'],
                'message': cd['message']
            }
            message = render_to_string('emails/listing_phone.html', context)
            to = [config.email]
            if listing.manager:
                to.append(listing.manager.email)
                
            subject = 'Нове повідомлення з сайту'
            sent = send_mail(subject, '', '', [to], html_message=message)
            if sent == 1:
                return JsonResponse({'status': 'ok'})

    except Listing.DoesNotExist:
        return JsonResponse({'status': 'bad', 'message': 'listing is not found'})
    return JsonResponse({'status': 'bad', 'message': 'bad response'})


@require_POST
def listing_visit(request, id):
    try:
        listing = Listing.objects.select_related('manager').get(id=id)
        form = ListingVisitForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            config = SiteConfiguration.objects.get()
        
            context = {
                'listing': listing,
                'phone': cd['phone'],
                'date': cd['date'],
                'time': cd['time'],
                'subject': 'Запис на перегляд'
            }
            message = render_to_string('emails/listing_phone.html', context)
            to = [config.email]
            if listing.manager:
                to.append(listing.manager.email)
                
            subject = 'Нове повідомлення з сайту'
            sent = send_mail(subject, '', '', [to], html_message=message)
            if sent == 1:
                return JsonResponse({'status': 'ok'})

    except Listing.DoesNotExist:
        return JsonResponse({'status': 'bad', 'message': 'listing is not found'})
    return JsonResponse({'status': 'bad', 'message': 'bad response'})


@require_POST
def listing_credit(request, id):
    try:
        listing = Listing.objects.select_related('manager').get(id=id)
        form = ListingPhoneForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            config = SiteConfiguration.objects.get()
        
            context = {
                'listing': listing,
                'phone': cd['phone'],
                'subject': 'Розрахувати іпотеку'
            }
            message = render_to_string('emails/listing_phone.html', context)
            to = [config.email]
            if listing.manager:
                to.append(listing.manager.email)
                
            subject = 'Нове повідомлення з сайту'
            sent = send_mail(subject, '', '', [to], html_message=message)
            if sent == 1:
                return JsonResponse({'status': 'ok'})

    except Listing.DoesNotExist:
        return JsonResponse({'status': 'bad', 'message': 'listing is not found'})
    return JsonResponse({'status': 'bad', 'message': 'bad response'})


@require_POST
def listing_check(request, id):
    try:
        listing = Listing.objects.select_related('manager').get(id=id)
        form = ListingPhoneForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            config = SiteConfiguration.objects.get()
        
            context = {
                'listing': listing,
                'phone': cd['phone'],
                'subject': 'Перевірити нерухомість перед покупкою'
            }
            message = render_to_string('emails/listing_phone.html', context)
            to = [config.email]
            if listing.manager:
                to.append(listing.manager.email)
                
            subject = 'Нове повідомлення з сайту'
            sent = send_mail(subject, '', '', [to], html_message=message)
            if sent == 1:
                return JsonResponse({'status': 'ok'})

    except Listing.DoesNotExist:
        return JsonResponse({'status': 'bad', 'message': 'listing is not found'})
    return JsonResponse({'status': 'bad', 'message': 'bad response'})

