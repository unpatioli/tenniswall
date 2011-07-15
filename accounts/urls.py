from django.conf.urls.defaults import patterns, url

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
)
