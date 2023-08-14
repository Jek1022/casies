import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from company.models import Company
from django.core.files.storage import FileSystemStorage


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = Company
    template_name = 'company/index.html'
    context_object_name = 'companies'
    queryset = Company.objects.all().filter(is_deleted=0)


@method_decorator(login_required, name='dispatch')
class DetailView(DetailView):
    model = Company
    template_name = 'company/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_LOGO_URL'] = settings.MEDIA_URL + 'logo/'  # Pass the MEDIA_URL to the template
        return context


@method_decorator(login_required, name='dispatch')
class CreateView(CreateView):
    model = Company
    template_name = 'company/create.html'
    fields = ['code', 'description', 'address_1', 'address_2', 'address_3', 'telephone_number', 'tin_number', 'logo']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('company.add_company'):
            raise Http404
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        logo_file = self.request.FILES.get('logo')
        if logo_file:
            folder = 'media/logo/'
            fs = FileSystemStorage(location=folder)  # defaults to MEDIA_ROOT
            fs.delete(folder + 'taxpayer-logo.jpg')
            self.object.logo = fs.save('taxpayer-logo.jpg', logo_file)

        self.object.entered_by = self.request.user
        self.object.modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('company:index'))


@method_decorator(login_required, name='dispatch')
class UpdateView(UpdateView):
    model = Company
    template_name = 'company/edit.html'
    fields = ['code', 'description', 'address_1', 'address_2', 'address_3', 'telephone_number', 'tin_number', 'logo']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('company.change_company'):
            raise Http404
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        logo_file = self.request.FILES.get('logo')
        if logo_file:
            folder = 'media/logo/'
            fs = FileSystemStorage(location=folder)  # defaults to MEDIA_ROOT
            fs.delete('taxpayer-logo.jpg')
            self.object.logo = fs.save('taxpayer-logo.jpg', logo_file)
            
        self.object.modified_by = self.request.user
        self.object.modified_date = datetime.datetime.now()
        self.object.save(update_fields=['description', 'address_1', 'address_2', 'address_3', 'telephone_number', 'tin_number', 'logo',
                                        'modified_by', 'modified_date'])
        return HttpResponseRedirect('/maintenance/company')
    

@method_decorator(login_required, name='dispatch')
class DeleteView(DeleteView):
    model = Company
    template_name = 'company/delete.html'
    success_url = reverse_lazy('company:index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('company.delete_company'):
            raise Http404
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.modified_by = self.request.user
        self.object.modified_date = datetime.datetime.now()
        self.object.is_deleted = 1
        self.object.status = 'I'
        self.object.save()
        