from django.urls import re_path
from . import views

app_name = 'datatransmission'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'portal/$', views.initiate, name='initiate'),
    re_path(r'portal/dataretrieval/$', views.DataRetrieval.as_view(), name='dataretrieval'),
    re_path(r'portal/datatransmit/$', views.DataTransmit.as_view(), name='datatransmit'),
    # re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # re_path(r'^create/$', views.CreateView.as_view(), name='create'),
    # re_path(r'^(?P<pk>[0-9]+)/update/$', views.UpdateView.as_view(), name='update'),
    # re_path(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteView.as_view(), name='delete'),
]