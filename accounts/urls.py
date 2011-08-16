from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from accounts.views import MyProfileView, MyProfileCreateView, ProfileView, MyProfileEditView, RegistrationView, ThankyouView

urlpatterns = patterns('',
    url(r'login/$',
        'accounts.views.login',
        { 'template_name': 'accounts/login.html', },
        name='accounts_login'
    ),
    url(r'logout/$',
        'django.contrib.auth.views.logout',
        { 'template_name': 'accounts/logged_out.html', },
        name='accounts_logout'
    ),
    url(r'register/$',
        RegistrationView.as_view(),
        name='accounts_register'
    ),
    url(r'thankyou/$',
        ThankyouView.as_view(),
        name='accounts_register_thankyou'
    ),

    url(r'profile/(?P<pk>\d+)/$',
        ProfileView.as_view(),
        name='accounts_profile'
    ),
    url(r'profile/$',
        login_required(MyProfileView.as_view()),
        name='accounts_my_profile'
    ),
    url(r'profile/new/$',
        login_required(MyProfileCreateView.as_view()),
        name='accounts_my_profile_new'
    ),
    url(r'profile/edit/$',
        login_required(MyProfileEditView.as_view()),
        name='accounts_my_profile_edit'
    ),
)
