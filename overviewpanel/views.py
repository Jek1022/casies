from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count, Subquery
from datetime import datetime
from cas.models import Cas
from datatransmission.models import InquiryResult

def index(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    data = {}
    if start_date and end_date:
        date_from, date_to = format_date(start_date, end_date)


        documents, row_count = get_row_count(date_from, date_to)
        transfer_rate, success_count = get_transfer_rate(documents, row_count)
        chart = get_chart_ratio(date_from, date_to, success_count)

        data["row"] = row_count
        data["transfer_rate"] = transfer_rate
        # print(chart)
        data["chart"] = chart

    return JsonResponse(data)


def get_row_count(date_from, date_to):
    data = {}
    documents = Cas.objects.filter(
        issue_date__range=(date_from, date_to),
        item_id=1
    ).values('id', 'document_type')
    
    si_count = documents.filter(document_type='01').count()
    dm_count = documents.filter(document_type='02').count()
    cm_count = documents.filter(document_type='03').count()
    sb_count = documents.filter(document_type='04').count()
    or_count = documents.filter(document_type='05').count()

    data = {
        "si_count": si_count,
        "dm_count": dm_count,
        "cm_count": cm_count,
        "sb_count": sb_count,
        "or_count": or_count,
        "dmcm_count": dm_count + cm_count,
    }
    return documents, data


def get_transfer_rate(documents, row_count):
    data = {}
    document_ids = [doc['id'] for doc in documents]

    result = InquiryResult.objects.filter(
        datatransmission__cas__id__in=document_ids
    )

    si_success_count = result.filter(datatransmission__cas__document_type='01', result_status_code='SUC001').count()
    si_total_count = row_count['si_count']
    si_rate = si_success_count / si_total_count * 100 if si_total_count else 0

    dm_success_count = result.filter(datatransmission__cas__document_type='02', result_status_code='SUC001').count()
    dm_total_count = row_count['dm_count']
    dm_rate = dm_success_count / dm_total_count * 100 if dm_total_count else 0

    cm_success_count = result.filter(datatransmission__cas__document_type='03', result_status_code='SUC001').count()
    cm_total_count = row_count['cm_count']
    cm_rate = cm_success_count / cm_total_count * 100 if cm_total_count else 0

    sb_success_count = result.filter(datatransmission__cas__document_type='04', result_status_code='SUC001').count()
    sb_total_count = row_count['sb_count']
    sb_rate = sb_success_count / sb_total_count * 100 if sb_success_count else 0

    or_success_count = result.filter(datatransmission__cas__document_type='05', result_status_code='SUC001').count()
    or_total_count = row_count['or_count']
    or_rate = or_success_count / or_total_count * 100 if or_success_count else 0
    
    success_count = si_success_count + dm_success_count + cm_success_count + sb_success_count + or_success_count
       
    data = {
        'si_rate': si_rate,
        'dm_rate': dm_rate,
        'cm_rate': cm_rate,
        'sb_rate': sb_rate,
        'or_rate': or_rate
    }

    return data, success_count


def get_chart_ratio(date_from, date_to, success_count):

    data = InquiryResult.objects.filter(
        datatransmission__cas__issue_date__range=(date_from, date_to),
        datatransmission__cas__item_id = 1,
    )

    processing_count = data.filter(process_status_code='02').count()
    failed_count = data.exclude(result_status_code='SUC001').count()

    transmitted = data.values('datatransmission__cas__id')

    ready_to_transmit = Cas.objects.filter(
        issue_date__range=(date_from, date_to),
        item_id=1
    ).values('id').exclude(
        id__in=Subquery(transmitted)
    ).count()
    
    data = {
        'ready_to_transmit': ready_to_transmit,
        'failed': failed_count,
        'processing': processing_count,
        'success': success_count
    }

    return data


def format_date(start_date, end_date):
    ''' Format date MM/DD/YYYY to YYYYMMDD '''
    try:
        formatted_start_date = datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y%m%d")
        formatted_end_date = datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y%m%d")

        return formatted_start_date, formatted_end_date
    except ValueError:
        return None, None
    