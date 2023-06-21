from django.http import JsonResponse
from props.models import SiteConfiguration
from .forms import FeadbackForm, ApplyForm
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMultiAlternatives


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