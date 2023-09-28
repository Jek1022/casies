# Create your views here.
import datetime
from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from eiscredential.models import EisCredential, Setting


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    template_name = 'eiscredential/index.html'
    context_object_name = 'credentials'

    def get_queryset(self):
        return Setting.objects.first()
    

@method_decorator(login_required, name='dispatch')
class DetailView(DetailView):
    model = EisCredential
    template_name = 'eiscredential/detail.html'
    context_object_name = 'eiscredential'

    def get_object(self):
        access_level = self.request.GET.get('_')
        return self.model.objects.filter(access_level=access_level).first()
    

@method_decorator(login_required, name='dispatch')
class UpdateView(UpdateView):
    model = EisCredential
    template_name = 'eiscredential/edit.html'
    fields = ['public_key', 'user_id', 'user_password', 'application_id', 'application_secret_key', 'accreditation_id', 'jws_key_id', 'force_refresh_token', 'authentication_url', 'invoices_url', 'inquiry_result_url']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('eiscredential.change_eiscredential'):
            raise Http404
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        force_refresh_token_state = form.cleaned_data['force_refresh_token']
        if force_refresh_token_state == 'on':
            self.object.force_refresh_token = 'true'
        else:
            self.object.force_refresh_token = 'false'

        self.object.modified_by = self.request.user
        self.object.modified_date = datetime.datetime.now()
        self.object.save(update_fields=['public_key', 'user_id', 'user_password', 'application_id', 'application_secret_key', 'accreditation_id', 'jws_key_id', 'force_refresh_token',
                                        'authentication_url', 'invoices_url', 'inquiry_result_url',
                                        'modified_by', 'modified_date'])
        return HttpResponseRedirect('/maintenance/eiscredential')
    

@csrf_exempt
def savesetting(request):
    if request.method == 'POST':
        mode = request.POST.get('mode', '')

        kwargs = {
            'modified_by_id': request.user.id,
            'modified_date': datetime.datetime.now()
        }
        if mode == 'LIVE':
            kwargs['config_eis_system_mode'] = 'Live'
        elif mode == 'SANDBOX':
            kwargs['config_eis_system_mode'] = 'Sandbox'

        Setting.objects.filter(pk=1).update(**kwargs)

    return redirect('eiscredential:index')
