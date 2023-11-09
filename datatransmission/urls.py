from django.urls import re_path
from . import views
from . import api_authentication

app_name = 'datatransmission'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'step-1/$', views.initiate, name='initiate'),
    re_path(r'retrieve/$', views.DataRetrieval.as_view(), name='dataretrieval'),
    re_path(r'launch/$', views.DataTransmit.as_view(), name='datatransmit'),
    re_path(r'eis/authentication/$', api_authentication.Authentication.as_view(), name='authentication'),
    re_path(r'eis/send/$', views.DataTransmit.as_view(), name='send'),
    re_path(r'eis/inquireinvoice/$', views.InquireInvoice.as_view(), name='inquireinvoice'),
    # re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # re_path(r'^create/$', views.CreateView.as_view(), name='create'),
    # re_path(r'^(?P<pk>[0-9]+)/update/$', views.UpdateView.as_view(), name='update'),
    # re_path(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteView.as_view(), name='delete'),
]