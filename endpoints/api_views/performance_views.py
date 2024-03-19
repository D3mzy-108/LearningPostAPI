import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from admin_app.models import MPerformance, Quest
from challenge_app.models import ChallengeScore
from website.models import User
from django.utils import timezone


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
        time = request.POST.get('time')
        if MPerformance.objects.filter(date=date, quest__id=quest_id, user__username=username).exists():
            mperformance = MPerformance.objects.filter(
                date=date, quest__id=quest_id, user__username=username).first()
            mperformance.total_answered += int(total_answered)
            mperformance.correctly_answered += int(correctly_answered)
            mperformance.wrongly_answered += int(wrongly_answered)
            mperformance.time += int(time)
            mperformance.save()
        else:
            mperformance = MPerformance()
            mperformance.user = user
            mperformance.quest = quest
            mperformance.date = date
            mperformance.total_answered = total_answered
            mperformance.correctly_answered = correctly_answered
            mperformance.wrongly_answered = wrongly_answered
            mperformance.time = time
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
    quest_performance_list = []
    for stats in mperformance:
        if len(quest_performance_list) > 0:
            quest_added = False
            for quest_stats in quest_performance_list:
                if quest_stats['quest'] == stats.quest.title:
                    quest_stats['total_answered'] += stats.total_answered
                    quest_stats['correctly_answered'] += stats.correctly_answered
                    quest_stats['wrongly_answered'] += stats.wrongly_answered
                    try:
                        quest_stats['time'] += stats.time
                    except:
                        pass
                    quest_added = True
            else:
                if quest_added == False:
                    quest_performance_list.append({
                        'quest': stats.quest.title,
                        'total_answered': stats.total_answered,
                        'correctly_answered': stats.correctly_answered,
                        'wrongly_answered': stats.wrongly_answered,
                        'time': stats.time,
                    })
        else:
            quest_performance_list.append({
                'quest': stats.quest.title,
                'total_answered': stats.total_answered,
                'correctly_answered': stats.correctly_answered,
                'wrongly_answered': stats.wrongly_answered,
                'time': stats.time,
            })
        list_length = len(performance_list)
        if list_length > 0 and stats.date == performance_list[list_length-1]['date']:
            performance_list[list_length -
                             1]['total_answered'] += stats.total_answered
            performance_list[list_length -
                             1]['correctly_answered'] += stats.correctly_answered
            performance_list[list_length -
                             1]['wrongly_answered'] += stats.wrongly_answered
            try:
                performance_list[list_length -
                                 1]['time'] += stats.time
            except:
                pass
        else:
            performance_list.append({
                'total_answered': stats.total_answered,
                'correctly_answered': stats.correctly_answered,
                'wrongly_answered': stats.wrongly_answered,
                'time': stats.time,
                'date': stats.date,
            })
    if len(performance_list) == 0:
        performance_list.append({
            'total_answered': 0,
            'correctly_answered': 0,
            'wrongly_answered': 0,
            'time': 0,
            'date': datetime.date.today(),
        })
    return JsonResponse({
        'success': True,
        'performance': performance_list,
        'quest_performance': quest_performance_list,
    })


def get_challenge_performance(request, username):
    end_date = timezone.now().date()
    start_date = end_date - datetime.timedelta(days=30)

    start_datetime = datetime.datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.datetime.combine(end_date, datetime.max.time())

    start_aware = timezone.make_aware(start_datetime)
    end_aware = timezone.make_aware(end_datetime)

    challenges = ChallengeScore.objects.filter(
        user__username=username,
        room__created_date__range=[start_aware, end_aware],
        room__is_active=False
    ).order_by('-id', '-room__created_date')
    challenge_list = []
    for challenge in challenges:
        recorded_scores = []
        for score in challenge.room.scores.all():
            recorded_scores.append({
                'isUser': score.user.username == username,
                'score': score.score_1 + score.score_2 + score.score_3 + score.score_4 + score.score_5,
            })
        sorted_scores = sorted(
            recorded_scores, key=lambda x: x['score'], reverse=True)
        rank = 1
        user_score = 0
        for sorted_score in sorted_scores:
            if sorted_score['isUser']:
                user_score = sorted_score['score']
                break
            else:
                rank += 1
        challenge_list.append({
            'room_slug': challenge.room.room_slug,
            'quest_cover': challenge.room.quest.cover.url,
            'quest_title': challenge.room.quest.title,
            'rank': rank,
            'score': user_score
        })
    return JsonResponse({
        'success': True,
        'challenges': challenge_list,
    })
