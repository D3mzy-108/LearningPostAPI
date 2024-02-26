import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from admin_app.models import MPerformance, Quest
from website.models import User


@csrf_exempt
def save_performance(request, username):
    if request.method == 'POST':
        quest_id = request.POST.get('testid')
        user = get_object_or_404(User, username=username)
        quest = get_object_or_404(Quest, id=quest_id)
        date = datetime.date.today()
        total_answered = request.POST.get('total_answered')
        correctly_answered = request.POST.get('correctly_answered')
        wrongly_answered = request.POST.get('wrongly_answered')
        if MPerformance.objects.filter(date=date, quest__id=quest_id).exists():
            mperformance = MPerformance.objects.filter(
                date=date, quest__id=quest_id, user__username=username).first()
            mperformance.total_answered += int(total_answered)
            mperformance.correctly_answered += int(correctly_answered)
            mperformance.wrongly_answered += int(wrongly_answered)
            mperformance.save()
        else:
            mperformance = MPerformance()
            mperformance.user = user
            mperformance.quest = quest
            mperformance.date = date
            mperformance.total_answered = total_answered
            mperformance.correctly_answered = correctly_answered
            mperformance.wrongly_answered = wrongly_answered
            mperformance.save()
        return JsonResponse({
            'success': True,
            'message': 'Statistics have been saved!',
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid Request!',
        })


def get_performance(request, username):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)
    user = get_object_or_404(User, username=username)
    questid = request.GET.get('questid') or ''
    if questid == '':
        mperformance = user.m_performance.filter(
            date__range=[start_date, end_date]).order_by('id', 'date')
    else:
        mperformance = user.m_performance.filter(quest__id=questid, date__range=[
                                                 start_date, end_date]).order_by('id', 'date')
    performance_list = []
    for stats in mperformance:
        list_length = len(performance_list)
        if stats.date == performance_list[list_length-1]['date']:
            performance_list[list_length -
                             1]['total_answered'] += stats.total_answered
            performance_list[list_length -
                             1]['correctly_answered'] += stats.correctly_answered
            performance_list[list_length -
                             1]['wrongly_answered'] += stats.wrongly_answered
        else:
            performance_list.append({
                'total_answered': stats.total_answered,
                'correctly_answered': stats.correctly_answered,
                'wrongly_answered': stats.wrongly_answered,
                'date': stats.date,
            })
    if len(performance_list) == 0:
        performance_list.append({
            'total_answered': 0,
            'correctly_answered': 0,
            'wrongly_answered': 0,
            'date': datetime.date.today(),
        })
    return JsonResponse({
        'success': True,
        'performance': performance_list,
    })
