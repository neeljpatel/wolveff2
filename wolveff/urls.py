from django.conf.urls import patterns, include, url
from django.contrib import admin
from league import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wolveff.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_player, name='upload'),
    url(r'^league/(?P<league_id>[0-9]+)/$', views.view_league, name='view-league'),
    url(r'^league/(?P<league_id>[0-9]+)/create/$', views.create_team, name='create-team'),
    url(r'^league/(?P<league_id>[0-9]+)/next/$', views.next_player, name='next-player'),
    url(r'^league/(?P<league_id>[0-9]+)/assign/$', views.assign_player, name='assign-player'),
    url(r'^league/(?P<league_id>[0-9]+)/garbage/$', views.trash_player, name='trash-player'),
    url(r'^league/(?P<league_id>[0-9]+)/move/$', views.move_player, name='move-player'),
    url(r'^admin/', include(admin.site.urls)),
)
