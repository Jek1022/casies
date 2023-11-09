import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import DocumentType


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = DocumentType
    template_name = 'documenttype/index.html'
    context_object_name = 'data_list'
    queryset = DocumentType.objects.all().filter(is_deleted=0)
    

@method_decorator(login_required, name='dispatch')
class DetailView(DetailView):
    model = DocumentType
    template_name = 'documenttype/detail.html'


@method_decorator(login_required, name='dispatch')
class CreateView(CreateView):
    model = DocumentType
    template_name = 'documenttype/create.html'
    fields = ['code', 'description']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('documenttype.add_documenttype'):
            raise Http404
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.entered_by = self.request.user
        self.object.modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('documenttype:index'))
    

@method_decorator(login_required, name='dispatch')
class UpdateView(UpdateView):
    model = DocumentType
    template_name = 'documenttype/edit.html'
    fields = ['code', 'description']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('documenttype.change_documenttype'):
            raise Http404
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.modified_by = self.request.user
        self.object.modified_date = datetime.datetime.now()
        self.object.save(update_fields=['description', 'modified_by', 'modified_date'])
        return HttpResponseRedirect('/maintenance/documenttype')
    

@method_decorator(login_required, name='dispatch')
class DeleteView(DeleteView):
    model = DocumentType
    template_name = 'documenttype/delete.html'
    success_url = reverse_lazy('documenttype:index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('documenttype.delete_documenttype'):
            raise Http404
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.modified_by = self.request.user
        self.object.modified_date = datetime.datetime.now()
        self.object.is_deleted = 1
        self.object.status = 'I'
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
