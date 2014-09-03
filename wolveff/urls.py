from django.conf.urls import patterns, include, url
from django.contrib import admin
from league import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wolveff.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^league/([0-9]+)/', views.view_league, name='view-league'),
    url(r'^league/([0-9]+)/next-player/', views.view_league, name='next-player'),
    url(r'^admin/', include(admin.site.urls)),
)
