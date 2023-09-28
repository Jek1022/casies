import hmac
import json
import time
import base64
import hashlib
import requests
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.conf import settings
from collections import defaultdict
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models import Sum, F, ExpressionWrapper, DateField, When, Case, Value, IntegerField, Q
from cas.models import Cas
from eiscredential.models import Setting
from .models import DataTransmissionModel
from .helpers import DataValidator, DecimalEncoder
from .api_authentication import Authentication

# Create your views here.
@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    # model = DataTransmission
    template_name = 'datatransmission/index.html'
    queryset = []


def initiate(request):
    is_authenticated = authenticate()
    if is_authenticated:
        cas_types = get_cas_type()
        document_types = get_document_type()
        setting = get_setting()
        
        context = {
            'initiated': True,
            'cas_types': cas_types,
            'document_types': document_types,
            'setting': setting
        }
        return render(request, 'datatransmission/multistep/data_retrieval.html', context)
    

def authenticate():

    is_authenticated = False
    if True:
        is_authenticated = True
    return is_authenticated


class DataRetrieval(ListView):
    template_name = 'datatransmission/multistep/data_retrieval.html'

    def post(self, request):
        if request.method == 'POST':
            try:
                issue_date_from = request.POST.get('issue_date_from')
                issue_date_to = request.POST.get('issue_date_to')
                cas_type = request.POST.get('cas_type')
                document_type = request.POST.get('document_type')

                cas_types = get_cas_type
                document_types = get_document_type
                
                # search in childmodel for fk relationship of parentmodel
                queryset = Cas.objects.filter(datatransmissionmodel__isnull=True)
                if issue_date_from and issue_date_to:
                    date_from, date_to = format_date(issue_date_from, issue_date_to)
                    if date_from and date_to:
                        queryset = queryset.filter(
                            Q(issue_date__gte=date_from) &
                            Q(issue_date__lte=date_to)
                        )

                if cas_type:
                    queryset = queryset.filter(cas_type=cas_type)

                if document_type:
                    queryset = queryset.filter(document_type=document_type)

                totals = queryset.filter(item_id=1).aggregate(
                    total_net_amount_payable=Sum('net_amount_payable')
                )

                json_queryset = serializers.serialize('json', queryset)
                json_data = [entry['pk'] for entry in json.loads(json_queryset)]

                validation_summary = []
                for datarow in queryset:

                    validated_row = DataValidator().validate(datarow)
                    if validated_row:
                        validation_summary.append({
                            'invoice_number':datarow.company_invoice_number,
                            'items': validated_row
                        })

                validated_invoices = {item['invoice_number'] for item in validation_summary}
                
                context = {
                    'queryset': queryset,
                    'json_data': json.dumps(json_data),
                    'validation_summary': validation_summary,
                    'validated_invoices': validated_invoices,
                    'cas_types': cas_types,
                    'document_types': document_types,
                    'setting': get_setting,
                    'totals': totals,
                    'form_fields': {
                        'issue_date_from': issue_date_from,
                        'issue_date_to': issue_date_to,
                        'cas_type': cas_type,
                        'document_type': document_type,
                    },
                }
                return render(request, self.template_name, context)
            except Exception as e:
                error_message = f"Error: {str(e)}"
                return JsonResponse({'error': error_message})

class DataTransmit(View):
    template_name = 'datatransmission/multistep/data_transmit.html'

    def post(self, request):
        invoices = request.POST.get('json_data', None)

        if invoices:
            context = self.ready(request, invoices)
            return render(request, self.template_name, context)
        else:
            try:
                invoice_id = request.POST.get('id', None),
                invoice_no = request.POST.get('invoice_number', None)
                
                if invoice_id is not None and invoice_no is not None:
                    response = self.send(invoice_id, invoice_no)
                    return JsonResponse(response)
                else:
                    return render(request, self.template_name)
            except Exception as e:
                return HttpResponse(f"Invalid request: {e}", status=400)
    
    def ready(self, request, invoices):
        try:
            queryset_ids = json.loads(invoices)
            
            queryset = Cas.objects.filter(pk__in=queryset_ids, item_id=1).values('pk', 'company_invoice_number').order_by('pk')
            querylist = list(queryset)
            grouped_list = defaultdict(list)
            # group pk by invoice number
            for item in querylist:
                grouped_list[
                    item['company_invoice_number']
                ].append(
                    item['pk']
                )
            # json_datalist = []
            # for invoice_number, pks in grouped_list.items():
            #     cas = Cas.objects.get(pk=pks[0]).to_json_format(pks)
            #     json_datalist.append(json.dumps(cas, cls=DecimalEncoder))
            
            context = {
                'setting': get_setting,
                'queryset': json.dumps(querylist)
            }
            return context
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Error: {str(e)}"
            }
        
    def send(self, invoice_id, invoice_no):
        time.sleep(1)
        if invoice_no is not None and invoice_id is not None:
            response = {
                'status': 'success',
                'message': f"<span class='text-primary'>Done invoice no. {invoice_no}</span>"
            }
        else:
            response = {
                'status': 'failed',
                'message': f'Failed sending invoice no. {invoice_no}'
            }

        return response
    

def get_cas_type():
    return [
        {'code': '01', 'description': 'iES Advertising'},
        {'code': '02', 'description': 'Circulation System'},
    ]


def get_document_type():
    return [
        {'code': '01', 'description': 'Sales Invoice'},
        {'code': '02', 'description': 'Debit Memo'},
        {'code': '03', 'description': 'Credit Memo'},
        {'code': '04', 'description': 'Service Billing'},
        {'code': '05', 'description': 'Official Receipt'},
    ]


def format_date(start_date, end_date):
    ''' Format date YYYY-MM-DD to YYYYMMDD '''
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")

        formatted_start_date = start_date.replace("-", "")
        formatted_end_date = end_date.replace("-", "")

        return formatted_start_date, formatted_end_date
    except ValueError:
        return None, None

        
def get_setting():
    return  Setting.objects.first()