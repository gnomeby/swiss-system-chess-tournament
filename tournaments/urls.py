from django.conf.urls import patterns, url

from tournaments import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/players/$', views.PlayersView.as_view(), name='players'),
    url(r'^(?P<pk>\d+)/rounds/$', views.rounds, name='rounds'),
)