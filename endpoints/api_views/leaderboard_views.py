from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from admin_app.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt


def get_top_10(request, username, testid):
    user = get_object_or_404(User, username=username)
    state = user.state
    country = user.country
    if not Leaderboard.objects.filter(
            user__pk=user.pk,
            quest__id=testid).exists():
        instance = Leaderboard()
        instance.user = user
        instance.quest = get_object_or_404(Quest, pk=testid)
        instance.save()
    leaderboard = Leaderboard.objects.filter(
        user__state=state,
        user__country=country,
        quest__id=testid)
    streak_leaderboard = leaderboard.order_by('-streak')
    questions_leaderboard = leaderboard.order_by('-questions_answered')
    streak_leaderboard_list = []
    added_items = 0
    you_found = False
    for item in streak_leaderboard:
        added_items += 1
        if added_items < 11:
            streak_leaderboard_list.append({
                'index': added_items,
                'user': {
                    'full_name': item.user.first_name,
                    'username': item.user.username,
                    'profile_photo': item.user.profile_photo,
                },
                'points': item.streak,
            })
            if item.user.username == user.username:
                you_found = True
        else:
            if you_found == False and item.user.username == user.username:
                streak_leaderboard_list.append({
                    'index': added_items,
                    'user': {
                        'full_name': item.user.first_name,
                        'username': item.user.username,
                        'profile_photo': item.user.profile_photo,
                    },
                    'points': item.streak,
                })
                break
    questions_leaderboard_list = []
    added_items = 0
    for item in questions_leaderboard:
        added_items += 1
        if added_items < 11:
            questions_leaderboard_list.append({
                'index': added_items,
                'user': {
                    'full_name': item.user.first_name,
                    'username': item.user.username,
                    'profile_photo': item.user.profile_photo,
                },
                'points': item.questions_answered,
            })
            if item.user.username == user.username:
                you_found = True
        else:
            if you_found == False and item.user.username == user.username:
                questions_leaderboard_list.append({
                    'index': added_items,
                    'user': {
                        'full_name': item.user.first_name,
                        'username': item.user.username,
                        'profile_photo': item.user.profile_photo,
                    },
                    'points': item.questions_answered,
                })
                break
    context = {
        'success': True,
        'region': state,
        'country': country,
        'streaks': streak_leaderboard_list,
        'questions': questions_leaderboard_list,
    }
    return JsonResponse(context)


@csrf_exempt
def update_rank(request, username, testid):
    if request.method == 'POST':
        streak = request.POST['streak']
        questions = request.POST['questions']
        m_instances = Leaderboard.objects.filter(
            user__username=username,
            quest__id=testid)
        if not m_instances.exists():
            instance = Leaderboard()
            instance.user = get_object_or_404(User, username=username)
            instance.quest = get_object_or_404(Quest, pk=testid)
            instance.streak = 0
            instance.questions_answered = 0
        else:
            instance = m_instances.first()
        if int(streak) > instance.streak:
            instance.streak = int(streak)
        instance.questions_answered += int(questions)
        instance.save()
        context = {
            'success': True,
            'message': 'Rank Updated!',
        }
    else:
        context = {
            'success': False,
            'message': 'Invalid Request!',
        }
    return JsonResponse(context)
