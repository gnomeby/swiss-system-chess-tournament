from django.conf.urls import patterns, url

from tournaments import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.details, name='details'),
    url(r'^(?P<pk>\d+)/rounds/$', views.rounds, name='rounds'),
    url(r'^(?P<pk>\d+)/standings/$', views.standings, name='standings'),
)