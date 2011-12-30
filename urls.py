from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from registration.forms import RegistrationFormUniqueEmail
from registration.views import register
from social.forms import Profile

admin.autodiscover()

urlpatterns = patterns('',
    # Utility urls
    # url(r'^comments/', include('django.contrib.comments.urls')),

    # Examples:
    # url(r'^$', 'tenniswall.views.home', name='home'),
    # url(r'^tenniswall/', include('tenniswall.foo.urls')),
    url(r'^$', include('welcome.urls')),

    url(r'^accounts/register/$',
        register,
        {'form_class': RegistrationFormUniqueEmail,},
        'registration_register',
    ),
    url(r'^accounts/', include('registration.urls')),

    url(r'^walls/', include('walls.urls')),
    url(r'^world/', include('world.urls')),

    url(r'^social/setup/$',
        'socialregistration.views.setup',
        { 'form_class': Profile },
        name='socialregistration_setup'
    ),
    url(r'^social/', include('socialregistration.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Static files
if settings.SERVE_STATIC:
    # Static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    # Media
    media_url = settings.MEDIA_URL
    if media_url[0] == '/':
        media_url = media_url[1:]
    if media_url[-1] != '/':
        media_url += '/'
    urlpatterns += patterns('django.views.static',
        url(r'^%(media_url)s(?P<path>.*)$' % {'media_url': media_url},
            'serve',
            {'document_root': settings.MEDIA_ROOT + '/'}
        )
    )
