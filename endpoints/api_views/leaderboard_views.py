import math
from multiprocessing.managers import BaseManager
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from admin_app.models import Leaderboard, User, Quest
from django.views.decorators.csrf import csrf_exempt

rank_types: list[str] = ['STREAK', 'QUESTIONS', 'XP']


def _build_leaderboard_list(rankings: BaseManager, rank_type: str, user: User) -> list[dict[str, any]]:
    """
    This function builds a list of rankings
    """
    ranking_list = []
    added_items = 0
    you_found = False
    for item in rankings:
        added_items += 1
        user_info = {
            'full_name': item.user.first_name,
            'username': item.user.username,
            'profile_photo': item.user.profile_photo,
        }
        points = 0
        if rank_type == rank_types[0]:
            points = item.streak
        elif rank_type == rank_types[1]:
            points = item.questions_answered
        elif rank_type == rank_types[2]:
            points = item.xp
        ranking_entry = {
            'index': added_items,
            'user': user_info,
            'points': points,
            'quest': item.quest.title,
            'date': item.date,
        }

        if added_items <= 10:
            ranking_list.append(ranking_entry)
            if item.user.username == user.username:
                you_found = True
        elif not you_found and item.user.username == user.username:
            ranking_list.append(ranking_entry)
            break
    return ranking_list


def _build_rankings(leaderboard: BaseManager, user: User) -> dict[str, any]:
    # SET REGION
    state = user.state
    country = user.country

    # ORDER RANKINGS
    streak_leaderboard = leaderboard.order_by('-streak')
    questions_leaderboard = leaderboard.order_by('-questions_answered')
    xp_leaderboard = leaderboard.order_by('-xp')

    # BUILD RANKING LIST
    streak_leaderboard_list = _build_leaderboard_list(
        streak_leaderboard, rank_types[0], user)
    questions_leaderboard_list = _build_leaderboard_list(
        questions_leaderboard, rank_types[1], user)
    xp_leaderboard_list = _build_leaderboard_list(
        xp_leaderboard, rank_types[2], user)

    return {
        'success': True,
        'region': state,
        'country': country,
        'streaks': streak_leaderboard_list,
        'questions': questions_leaderboard_list,
        'xp_leaderboard': xp_leaderboard_list,
    }


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

    return JsonResponse(_build_rankings(leaderboard=leaderboard, user=user))


def get_top_10_global(request, username):
    user = get_object_or_404(User, username=username)
    state = user.state
    country = user.country
    leaderboard = Leaderboard.objects.filter(
        user__state=state,
        user__country=country)

    return JsonResponse(_build_rankings(leaderboard=leaderboard, user=user))


@csrf_exempt
def update_rank(request, username, testid):
    """
    Collects the following details:
    'streak' - The maximum streak attained by the user during the quest
    'questions' - The number of questions the user answered correctly during that quest attempt
    'score' - A value between 0 and 1 representing the user's score based on their percentage.
       Example: User scored 73% on the quest.
       score = 73/100
           = 0.73
    """
    if request.method == 'POST':
        try:
            streak = request.POST['streak'] or '0'
            questions = request.POST['questions'] or '0'
            score = request.POST['score'] or '0'
            m_instances = Leaderboard.objects.filter(
                user__username=username,
                quest__id=testid)
            if not m_instances.exists():
                instance = Leaderboard()
                instance.user = get_object_or_404(User, username=username)
                instance.quest = get_object_or_404(Quest, pk=testid)
                instance.streak = 0
                instance.questions_answered = 0
                instance.xp = 0
            else:
                instance = m_instances.first()
            if int(streak) > instance.streak:
                instance.streak = int(streak)
            instance.questions_answered += int(questions)
            instance.xp += math.floor((30 * float(score)))
            instance.save()
            context = {
                'success': True,
                'message': 'Rank Updated!',
            }
        except Exception as error:
            print(error)
            context = {
                'success': False,
                'message': 'Invalid data provided!',
            }
    else:
        context = {
            'success': False,
            'message': 'Invalid Request!',
        }
    return JsonResponse(context)
