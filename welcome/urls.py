from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('welcome.views',
    url(r'^$', 'index', name='root'),
)