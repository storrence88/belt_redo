from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^home$', views.homepage),
    # url(r'^user/(?P<id>\d+)$', views.view_friend),
    # url(r'^user/add/(?P<id>\d+)$', views.add_friend),
    # url(r'^user/delete/(?P<id>\d+)$', views.delete_friend)
]