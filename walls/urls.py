from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from walls.views import AddWallView, EditWallView,\
    CommentedWallDetailView, DeleteWallView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$',
        CommentedWallDetailView.as_view(),
        name='walls_detail'
    ),
    url(r'^(?P<pk>\d+)/edit/$',
        login_required(EditWallView.as_view()),
        name='walls_edit'
    ),
    url(r'^(?P<pk>\d+)/delete/$',
        login_required(DeleteWallView.as_view()),
        name='walls_delete'
    ),
    url(r'^add/$',
        login_required(AddWallView.as_view()),
        name='walls_add'
    ),

    url(r'^bbox.json/$',
        'walls.views.bbox',
        name='walls_bbox'
    ),
)
