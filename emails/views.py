from django.http import JsonResponse
from props.models import SiteConfiguration
from .forms import FeadbackForm
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.core.mail import send_mail


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
