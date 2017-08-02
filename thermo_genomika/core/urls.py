from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^charts/$', views.charts, name='charts'),
    url(
        r'^dashboards/(?P<local_id>[0-9]+)/$',
        views.dashboards,
        name='dashboards'),
    url(
        r'^gui_dashboard/(?P<local_id>[0-9]+)/$',
        views.gui_dashboard,
        name='gui_dashboard'),
]
