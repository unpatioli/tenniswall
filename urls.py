from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tenniswall.views.home', name='home'),
    # url(r'^tenniswall/', include('tenniswall.foo.urls')),
    url(r'^$', include('welcome.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^walls/', include('walls.urls')),
    url(r'^world/', include('world.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Static files
if settings.SERVE_STATIC:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
