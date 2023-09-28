from django.urls import re_path
from . import views

app_name = 'eiscredential'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^detail/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^(?P<pk>[0-9]+)/update/$', views.UpdateView.as_view(), name='update'),
    re_path(r'^savesetting/$', views.savesetting, name='savesetting'),
]