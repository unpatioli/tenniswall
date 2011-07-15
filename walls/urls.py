from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from walls.views import AddView

urlpatterns = patterns('',
    url(r'^$', 'walls.views.index', name='walls_index'),

    url(r'^add/$', login_required(AddView.as_view()), name='walls_add'),
)
