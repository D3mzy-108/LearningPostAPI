from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Prefetch
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from website.models import User
from admin_app.models import Quest, Question
from challenge_app.models import ArenaRoom, Participants


@require_POST
@csrf_exempt
def join_room(request):
    room_name = request.POST.get('room_name')
    username = request.POST.get('username')
    # FIND ROOM INSTANCE
    room = ArenaRoom.objects.filter(
        room_name=room_name, is_active=True)
    if not room.exists():
        room_instance = ArenaRoom()
        room_instance.room_name = room_name
        room_instance.save()
    lobby = ArenaRoom.objects.filter(
        room_name=room_name, is_active=True).first()
    user = get_object_or_404(User, username=username)
    instance = Participants()
    instance.user = user
    instance.room = lobby
    instance.save()
    if lobby.quest:
        quest = {
            'testid': lobby.quest.pk,
            'title': lobby.quest.title,
            'cover': lobby.quest.cover.url,
        }
    else:
        quest = {
            'testid': None,
            'title': '',
            'cover': '',
        }
    return JsonResponse({
        'success': True,
        'room_slug': lobby.room_slug,
        'room_name': lobby.room_name,
        'quest': quest,
    })


def find_open_rooms(request, username):
    user = get_object_or_404(User, username=username)
    friends = user.friends.all()
    active_rooms = ArenaRoom.objects.filter(is_active=True)
    arenas_list = []
    for room in active_rooms:
        friend_participants = Participants.objects.filter(
            room__pk=room.pk, user__in=friends)
        arenas_list.append({
            'room_slug': room.room_slug,
            'room_name': room.room_name,
            'quest': {
                'testid': room.quest.pk,
                'title': room.quest.title,
                'cover': room.quest.cover.url,
            },
            'friend': {
                'profilePhoto': friend_participants.first().user.profile_photo,
                'display': f'{friend_participants.first().user.first_name} {f"and {friend_participants.count() - 1} others" if friend_participants.count() > 1 else ""}',
            } if friend_participants.exists() else None,
        })
    return JsonResponse({
        'success': True,
        'active_arenas': arenas_list,
    })


@require_POST
@csrf_exempt
def change_quest(request):
    room_name = request.POST.get('room_name')
    testid = request.POST.get('testid')
    room = ArenaRoom.objects.filter(
        room_name=room_name, is_active=True)
    instance = room.first()
    instance.quest = get_object_or_404(Quest, pk=testid)
    instance.save()
    return JsonResponse({
        'success': True,
        'quest': {
            'testid': instance.quest.pk,
            'title': instance.quest.title,
            'cover': instance.quest.cover.url,
        }
    })


def get_challenge_questions(request, testid: int, limit: int):
    questions = []
    all_questions = Question.objects.filter(quest__pk=testid).order_by('?')
    random_items = all_questions[:limit]
    for question in random_items:
        diagram_url = None
        if question.diagram:
            diagram_url = question.diagram.url
        questions.append({
            'questionid': question.pk,
            'comprehension': question.comprehension,
            'diagram': diagram_url,
            'question': question.question,
            'a': question.a,
            'b': question.b,
            'c': question.c,
            'd': question.d,
            'answer': question.answer,
        })
    context = {
        'success': True,
        'questions': questions,
    }
    return JsonResponse(context)


@require_POST
@csrf_exempt
def save_score(request):
    room_name = request.POST.get('room_name')
    username = request.POST.get('username')
    score = request.POST.get('score')
    participant = Participants.objects.filter(
        room__room_name=room_name, user__username=username).order_by('-id')
    if participant.exists():
        instance = participant.first()
        instance.score = score
        instance.save()
    return JsonResponse({'success': True})


def get_participants(request, room_name, username):
    participants = Participants.objects.filter(
        room__room_name=room_name, room__is_active=True).order_by('-score')
    user = get_object_or_404(User, username=username)
    friends = user.friends.filter(online=True)
    return JsonResponse({
        'success': True,
        'participants': [
            {
                'profilePhoto': participant.user.profile_photo,
                'displayName': participant.user.first_name,
                'username': participant.user.username,
                'score': participant.score,
            } for participant in participants
        ],
        'friends': [
            {
                'profilePhoto': friend.profile_photo,
                'displayName': friend.first_name,
                'username': friend.username,
            } for friend in friends
        ]
    })


def _close_room(room: ArenaRoom | None):
    if not room:
        return
    participants = Participants.objects.filter(room__room_slug=room.room_slug)
    # CHECK IF ANY PARTICIPANT HAS A SCORE HIGHER THAN 0
    # THIS IS TO PROVE THAT THE CHALLENGE WAS ACTUALLY ATTEMPTED
    if participants.filter(score__gt=0).exists():
        room.is_active = False
        room.save()
    # IF SUCH PARTICIPANT DOESN'T EXIST, DELETE THE ROOM AND ITS PARTICIPANTS
    else:
        room.delete()


def leave_arena(request, room_name):
    room = ArenaRoom.objects.filter(room_name=room_name, is_active=True)
    if room.exists():
        instance = room.first()
        _close_room(instance)
    return JsonResponse({
        'success': True,
        'message': 'Arena has been closed',
    })


def challenge_history(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'success': False, 'error': 'Username not provided'}, status=400)

    rooms = ArenaRoom.objects.filter(scores__user__username=username).order_by('-created_date').prefetch_related(
        Prefetch(
            'scores',
            queryset=Participants.objects.order_by(
                '-score').select_related('user'),
            to_attr='ranked_scores'
        ),
        'quest'
    )

    challenges = []
    for room in rooms:
        user_position = None
        participants = []
        for index, participant in enumerate(room.ranked_scores):
            # RECORD CURRENT USER'S RANK
            if participant.user.username == username:
                user_position = index + 1
            # ADD PARTICIPANT TO PARTICIPANTS LIST
            participants.append({
                'profilePhoto': participant.user.profile_photo,
                'displayName': participant.user.first_name,
                'username': participant.user.username,
                'score': participant.score,
            })

        challenges.append({
            'quest': {
                'cover': room.quest.cover.url if room.quest and hasattr(room.quest, 'cover') else '',
                'title': room.quest.title if room.quest else '',
            },
            'date': room.created_date.strftime('%d %B, %y'),
            'position': user_position,
            'participants': participants,
        })

    return JsonResponse({'success': True, 'challenges': challenges})
