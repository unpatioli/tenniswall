from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('world.views',
    url(r'^$', 'index', name='world'),
)