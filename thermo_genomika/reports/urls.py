
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^full-report$', views.report, name='report'),
    url(r'^audited-report$', views.audited_report, name='audited_report'),
]
