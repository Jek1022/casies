# Create your views here.
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.conf import settings

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from eiscredential.models import EisCredential


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    template_name = 'eiscredential/index.html'
    context_object_name = 'credentials'
    queryset = EisCredential.objects.all()


@method_decorator(login_required, name='dispatch')
class DetailView(DetailView):
    model = EisCredential
    template_name = 'eiscredential/detail.html'

    def get_object(self):
        object_id = self.request.GET.get('m')
        data = self.model.objects.filter(access_level=object_id).first()
        # continue dito to show cred details 09/22/2023
        return data
    

@method_decorator(login_required, name='dispatch')
class UpdateView(UpdateView):
    model = EisCredential
    template_name = 'eiscredential/edit.html'
    fields = ['code', 'description', 'address_1', 'address_2', 'address_3', 'telephone_number', 'tin_number', 'logo']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('company.change_company'):
            raise Http404
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
            
        self.object.modified_by = self.request.user
        self.object.modified_date = datetime.datetime.now()
        self.object.save(update_fields=['description', 'address_1', 'address_2', 'address_3', 'telephone_number', 'tin_number', 'logo',
                                        'modified_by', 'modified_date'])
        return HttpResponseRedirect('/maintenance/company')