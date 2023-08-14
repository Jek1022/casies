import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from cas.models import Cas


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = Cas
    template_name = 'cas/index.html'
    queryset = Cas.objects.all().filter(is_deleted=0)