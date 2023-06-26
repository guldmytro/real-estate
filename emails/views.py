from django.http import JsonResponse
from props.models import SiteConfiguration
from .forms import FeadbackForm, ApplyForm, ReviewForm
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMultiAlternatives
from managers.models import Manager
from django.core.validators import validate_email
from django import forms


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
    

def manager_add_review(request, id):
    review_form = ReviewForm(request.POST)
    if review_form.is_valid():
        review_form.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'formErrors': review_form.errors})
