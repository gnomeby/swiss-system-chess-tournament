from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.http.response import HttpResponseRedirect
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$',  lambda request: HttpResponseRedirect('/tournaments/')),
    url(r'^tournaments/', include('tournaments.urls', namespace="tournaments")),
    # url(r'^ss_chess_tour/', include('ss_chess_tour.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
