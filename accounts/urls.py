from django.conf.urls.defaults import patterns, url
from accounts.views import MyProfileView, MyProfileCreateView, ProfileView

urlpatterns = patterns('',
    url(r'login/$',
        'django.contrib.auth.views.login',
        { 'template_name': 'accounts/login.html', },
        name='accounts_login'
    ),

    url(r'logout/$',
        'django.contrib.auth.views.logout',
        { 'template_name': 'accounts/logged_out.html', },
        name='accounts_logout'
    ),

    url(r'register/$',
        'accounts.views.register',
        name='accounts_register'
    ),

    url(r'profile/(?P<pk>\d+)/$',
        ProfileView.as_view(),
        name='accounts_profile'
    ),
    url(r'profile/$',
        MyProfileView.as_view(),
        name='accounts_my_profile'
    ),
    url(r'profile/new/$',
        MyProfileCreateView.as_view(),
        name='accounts_my_profile_new'
    ),
)
