
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^reports/$', views.report, name='reports'),
]
