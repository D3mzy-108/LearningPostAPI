import csv
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import SmartLinkKB
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def smartlinks(request):
    search_val = request.GET.get('s') or ''
    smartlinks = SmartLinkKB.objects.filter(statement__icontains=search_val)
    paginator = Paginator(smartlinks, 100)
    page = request.GET.get('page')
    if page == None or int(page) > paginator.num_pages:
        page = 1
    displayed_sl = paginator.page(page)
    context = {
        'smartlinks': displayed_sl,
        'paginator': displayed_sl,
        'page': page,
    }
    return render(request, 'smartlink/smartlinks.html', context)


def chunks(lst):
    """Yields successive n-sized chunks from lst."""
    for i in range(0, len(lst), 800):
        yield lst[i:i + 800]


@login_required
def bulk_upload_smartlinks(request):
    if request.method == 'POST' and request.FILES['sl_upload_file']:
        uploaded_file = request.FILES['sl_upload_file']

        if uploaded_file.name.lower().endswith('.json'):
            # Read and process the uploaded JSON file
            data = json.load(uploaded_file)
            data_list = [{"statement": statement, "definition": definition}
                         for statement, definition in data.items()]
            for chunk in chunks(data_list):
                smartlink_objects = []

                for item in chunk:
                    smartlink_objects.append(SmartLinkKB(**item))

                SmartLinkKB.objects.bulk_create(smartlink_objects)
        elif uploaded_file.name.lower().endswith('.tsv'):
            # Read and process the uploaded TSV file
            decoded_file = uploaded_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter='\t')
            data_list = [row for row in reader]
            for chunk in chunks(data_list):
                smartlink_objects = []

                for statement, definition in chunk:
                    mapped_data = {
                        "statement": statement,
                        "definition": definition,
                    }
                    smartlink_objects.append(SmartLinkKB(**mapped_data))

                SmartLinkKB.objects.bulk_create(smartlink_objects)
            # for row in reader:
            #     statement, definition = row
            #     SmartLinkKB.objects.create(
            #         statement=statement, definition=definition)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('smartlinks')
    else:
        return redirect(request.META.get('HTTP_REFERER'))


def find_smartlinks(request):
    search_val = request.GET.get('s') or ''
    smartlinks = SmartLinkKB.objects.filter(statement__iexact=search_val)
    smartlink_list = []
    for sl in smartlinks:
        smartlink_list.append({
            'term': sl.statement,
            'definition': sl.definition,
        })
    context = {
        'smartlinks': smartlink_list,
    }
    return JsonResponse(context)
