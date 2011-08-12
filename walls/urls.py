from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from walls.views import AddWallView, EditWallView,\
    CommentedWallDetailView, DeleteWallView, WallImagesListView, WallImagesDetailView, WallImagesEditView, WallImagesDeleteView, WallImagesAddView, WallImagesListEditView

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

    url(r'^(?P<wall_pk>\d+)/images/$',
        WallImagesListView.as_view(),
        name='walls_images_list'
    ),
    url(r'^(?P<wall_pk>\d+)/images/edit/$',
        login_required(WallImagesListEditView.as_view()),
        name='walls_images_list_edit'
    ),
    url(r'^(?P<wall_pk>\d+)/images/(?P<pk>\d+)/$',
        WallImagesDetailView.as_view(),
        name='walls_images_detail'
    ),
    url(r'^(?P<wall_pk>\d+)/images/(?P<pk>\d+)/edit/$',
        login_required(WallImagesEditView.as_view()),
        name='walls_images_edit'
    ),
    url(r'^(?P<wall_pk>\d+)/images/(?P<pk>\d+)/delete/$',
        login_required(WallImagesDeleteView.as_view()),
        name='walls_images_delete'
    ),
    url(r'^(?P<wall_pk>\d+)/images/add/$',
        login_required(WallImagesAddView.as_view()),
        name='walls_images_add'
    ),

    url(r'^bbox.json/$',
        'walls.views.bbox',
        name='walls_bbox'
    ),
)
