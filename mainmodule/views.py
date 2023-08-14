import datetime
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from mainmodule.models import Mainmodule
from django.utils import timezone


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = Mainmodule
    template_name = 'mainmodule/index.html'
    context_object_name = 'mainmodules'
    queryset = Mainmodule.objects.all().filter(is_deleted=0)


@method_decorator(login_required, name='dispatch')
class DetailView(DetailView):
    model = Mainmodule
    template_name = 'mainmodule/detail.html'


@method_decorator(login_required, name='dispatch')
class CreateView(CreateView):
    model = Mainmodule
    template_name = 'mainmodule/create.html'
    fields = ['code', 'description', 'sort_number', 'division', 'icon_file']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('mainmodule.add_mainmodule'):
            raise Http404
        return super(CreateView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['division_choices'] = Mainmodule.DIVISION_CHOICES
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.enterby = self.request.user
        self.object.modifyby = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('mainmodule:index'))


@method_decorator(login_required, name='dispatch')
class UpdateView(UpdateView):
    model = Mainmodule
    template_name = 'mainmodule/edit.html'
    fields = ['code', 'description', 'sort_number', 'division', 'icon_file']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('mainmodule.change_mainmodule'):
            raise Http404
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modifyby = self.request.user
        self.object.modifydate = datetime.datetime.now()
        self.object.save(update_fields=['description', 'sort_number', 'division', 'icon_file',
                                        'modified_by', 'modified_date'])
        return HttpResponseRedirect(reverse('mainmodule:index'))


@method_decorator(login_required, name='dispatch')
class DeleteView(DeleteView):
    model = Mainmodule
    template_name = 'mainmodule/delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('mainmodule.delete_mainmodule'):
            raise Http404
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.modifyby = self.request.user
        self.object.modifydate = datetime.datetime.now()
        self.object.is_deleted = 1
        self.object.status = 'I'
        self.object.save()
        return HttpResponseRedirect(reverse('mainmodule:index'))