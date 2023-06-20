from news.models import PostModel
from django.urls import reverse


class Analytic(PostModel):
    class Meta:
        verbose_name = 'Analytic'
        verbose_name_plural = 'Analytics'

    def get_absolute_url(self):
        return reverse('analytics:detail', kwargs={'slug': self.slug})