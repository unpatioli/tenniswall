from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('welcome.views',
    url(r'^$',
        TemplateView.as_view(
            template_name='welcome/index.html'
        ),
        name='root'
    ),
)
