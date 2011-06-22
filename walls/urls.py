from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'walls.views.index', name='walls_index'),
    url(r'^add/$', 'walls.views.add', name='walls_add'),
    url(r'^(?P<wall_id>\w+)/$', 'walls.views.show', name='walls_show'),
)