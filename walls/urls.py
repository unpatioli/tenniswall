from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'walls.views.index', name='walls_index'),
)