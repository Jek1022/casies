import datetime
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, Http404
from module.models import Module, Activitylogs
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from mainmodule.models import Mainmodule
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.db import connection
from collections import namedtuple


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = Module
    template_name = 'module/index.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        return Module.objects.all().filter(is_deleted=0).order_by('-pk')


@method_decorator(login_required, name='dispatch')
class DetailView(DetailView):
    model = Module
    template_name = 'module/detail.html'


@method_decorator(login_required, name='dispatch')
class CreateView(CreateView):
    model = Module
    template_name = 'module/create.html'
    fields = ['code', 'description', 'mainmodule', 'django_content_type', 'name', 'segment']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('module.add_module'):
            raise Http404
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['mainmodule'] = Mainmodule.objects.filter(is_deleted=0).order_by('description')
        context['django_content_type'] = ContentType.objects.\
            exclude(pk__in=[1, 2, 5, 6]).order_by('app_label')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.enterby = self.request.user
        self.object.modifyby = self.request.user
        self.object.save()
        return HttpResponseRedirect('/module')


@method_decorator(login_required, name='dispatch')
class UpdateView(UpdateView):
    model = Module
    template_name = 'module/edit.html'
    fields = ['code', 'description', 'mainmodule', 'django_content_type', 'name', 'segment']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('module.change_module'):
            raise Http404
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['mainmodule'] = Mainmodule.objects.filter(is_deleted=0).order_by('description')
        context['django_content_type'] = ContentType.objects.\
            exclude(pk__in=[1, 2, 5, 6]).order_by('app_label')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modifyby = self.request.user
        self.object.modifydate = datetime.datetime.now()
        self.object.save(update_fields=['description', 'mainmodule', 'django_content_type',
                                        'name', 'segment',
                                        'modifyby', 'modifydate'])
        return HttpResponseRedirect('/module')


@method_decorator(login_required, name='dispatch')
class DeleteView(DeleteView):
    model = Module
    template_name = 'module/delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('module.delete_module'):
            raise Http404
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.modifyby = self.request.user
        self.object.modifydate = datetime.datetime.now()
        self.object.is_deleted = 1
        self.object.status = 'I'
        self.object.save()
        return HttpResponseRedirect('/module')