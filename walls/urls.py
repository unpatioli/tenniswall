from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import  ListView
from walls.models import Wall
from walls.views import AddWallView, IndexView, EditWallView,\
    CommentedWallDetailView

urlpatterns = patterns('',
    url(r'^$',
        IndexView.as_view(),
        name='walls_index'
    ),
    url(r'free/$',
        ListView.as_view(
            queryset=Wall.free.all()
        ),
        name='walls_free'
    ),
    url(r'paid/$',
        ListView.as_view(
            queryset=Wall.paid.all()
        ),
        name='walls_paid'
    ),

    url(r'^(?P<pk>\d+)/$',
        CommentedWallDetailView.as_view(),
        name='walls_detail'
    ),
    url(r'^(?P<pk>\d+)/edit/$',
        login_required(EditWallView.as_view()),
        name='walls_edit'
    ),
    url(r'^add/$',
        login_required(AddWallView.as_view()),
        name='walls_add'
    ),
)
