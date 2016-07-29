from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^charts/$', views.charts, name='charts'),
    url(r'^reports/$', views.report, name='reports'),
]
