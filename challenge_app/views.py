from website.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from admin_app.models import Quest, Question
from challenge_app.models import ArenaRoom, Participants
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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
            'testid': quest.pk,
            'title': quest.title,
            'cover': quest.cover.url,
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
        room__room_name=room_name, room__is_active=True)
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


def leave_arena(request, room_name):
    room = ArenaRoom.objects.filter(room_name=room_name, is_active=True)
    if room.exists():
        instance = room.first()
        instance.is_active = False
        instance.save()
    return JsonResponse({
        'success': True,
        'message': 'Arena has been closed',
    })
