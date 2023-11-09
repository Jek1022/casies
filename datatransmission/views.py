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
from datatransmission.api_resultinquiry import ResultInquiry
from eiscredential.models import Setting
from castype.models import CasType
from documenttype.models import DocumentType
from .models import DataTransmission
from .helpers import DataValidator, DecimalEncoder
from .api_authentication import Authentication
from .api_invoices import Transmit

# Create your views here.
@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
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
                queryset = Cas.objects.filter(datatransmission_cas__isnull=True)
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

                invoices = queryset.filter(item_id=1)
                invoice_count = invoices.count()

                totals = invoices.aggregate(
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
                    'invoice_count': invoice_count,
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
            print('diiin', invoices)
            context = self.ready(request, invoices)
            return render(request, self.template_name, context)
        else:
            print('wray')
            try:
                data = json.loads(request.body)
                invoice_ids = data.get('invoice_ids', []),
                invoice_no = data.get('invoice_number', None)
                
                if invoice_ids[0] and invoice_no is not None:
                    response = self.send(request, invoice_ids[0], invoice_no)
                    print('response', response)
                    return JsonResponse(response)
                
                else:
                    return render(request, self.template_name)
            except Exception as e:
                return HttpResponse(f"Invalid request, {e}.", status=400)
    
    def ready(self, request, invoices):
        try:
            queryset_ids = json.loads(invoices)
            
            queryset = Cas.objects.filter(pk__in=queryset_ids).values('pk', 'company_invoice_number').order_by('pk', 'item_id')
            querylist = list(queryset)
            grouped_list = defaultdict(list)
            # group pk by invoice number
            for item in querylist:
                grouped_list[
                    item['company_invoice_number']
                ].append(
                    item['pk']
                )

            items = []
            for inv, ids in grouped_list.items():
                items.append({'company_invoice_number': inv, 'pk': ids})
                
            context = {
                'setting': get_setting,
                'items': json.dumps(items)
            }
            return context
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Error: {str(e)}"
            }
        
    def send(self, request, invoice_ids, invoice_no):
        # time.sleep(1)
        if invoice_ids and invoice_no is not None:
            
            json_format = Cas.objects.get(pk=invoice_ids[0]).to_json_format(invoice_ids)
            
            response = Transmit().execute(request, invoice_no, invoice_ids, json_format)
            # if response['status']:
                
        else:
            response = {
                'status': 'failed',
                'message': f'Failed sending invoice no. {invoice_no}'
            }

        return response
    

class InquireInvoice(View):
    template_name = 'datatransmission/multistep/result_inquiry.html'
    
    def post(self, request):
        transmitted_invoices = request.POST.get('transmitted_invoices', None)

        if transmitted_invoices:
            context = {'transmitted_invoices': transmitted_invoices}
            return render(request, self.template_name, context)
        else:
            try:
                data = json.loads(request.body)
                invoice_ids = data.get('invoice_ids', []),
                invoice_no = data.get('invoice_number', None)
                
                if invoice_ids[0] and invoice_no is not None:
                    response = self.send(request, invoice_ids[0], invoice_no)
                    
                    return JsonResponse(response)
                
                else:
                    return render(request, self.template_name)
            except Exception as e:
                return HttpResponse(f"Invalid request, {e}.", status=400)
            
    def send(self, request, invoice_ids, invoice_no):
        # time.sleep(1)
        if invoice_ids and invoice_no is not None:
            
            data = DataTransmission.objects.get(cas_id=invoice_ids[0])
            submit_id = data.ref_submit_id
            data_id = data.pk
            response = ResultInquiry().get_status(request, submit_id, data_id, invoice_no)
             
        else:
            response = {
                'status': 'failed',
                'message': f'Failed requesting status of invoice no. {invoice_no}'
            }

        return response
    

def get_cas_type():
    castype = CasType.objects.filter(is_deleted=0).values('code', 'description')
    return castype
    # return [
    #     {'code': '01', 'description': 'iES Advertising'},
    #     {'code': '02', 'description': 'Circulation System'},
    # ]


def get_document_type():
    documenttype = DocumentType.objects.filter(is_deleted=0).values('code', 'description')
    return documenttype
    # return [
    #     {'code': '01', 'description': 'Sales Invoice'},
    #     {'code': '02', 'description': 'Debit Memo'},
    #     {'code': '03', 'description': 'Credit Memo'},
    #     {'code': '04', 'description': 'Service Billing'},
    #     {'code': '05', 'description': 'Official Receipt'},
    # ]


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