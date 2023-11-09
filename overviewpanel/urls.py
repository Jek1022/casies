from django.urls import re_path
from .import views

app_name = 'overviewpanel'

urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^get_row_count/$', views.get_row_count, name='get_row_count'),
]