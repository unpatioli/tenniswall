from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from walls.views import AddPaidView, AddFreeView

urlpatterns = patterns('',
    url(r'^$',
        'walls.views.index',
        name='walls_index'
    ),
    url(r'paid/$',
        'walls.views.index',
        name='walls_paid'
    ),
    url(r'free/$',
        'walls.views.index',
        name='walls_free'
    ),

    url(r'^paid/add/$',
        login_required(AddPaidView.as_view()),
        name='walls_paid_add'
    ),
    url(r'^free/add/$',
        login_required(AddFreeView.as_view()),
        name='walls_free_add'
    )
)
