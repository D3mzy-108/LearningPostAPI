from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from admin_app.models import Quest, Question
from challenge_app.models import ChallengeRoom, ChallengeScore
from django.views.decorators.csrf import csrf_exempt

from website.models import User


def create_room(request):
    room_name = request.GET.get('room_name')
    testid = request.GET.get('testid')
    # CREATE ROOM INSTANCE
    if not ChallengeRoom.objects.filter(room_name=room_name, is_active=True).exists():
        room_instance = ChallengeRoom()
        room_instance.room_name = room_name
        room_instance.quest = get_object_or_404(Quest, id=testid)
        room_instance.save()
        return JsonResponse({
            'success': True,
            'room_slug': room_instance.room_slug,
            'room_name': room_instance.room_name,
        })
    else:
        return JsonResponse({
            'success': False,
        })


def join_room(request):
    room_name = request.GET.get('room_name')
    # FIND ROOM INSTANCE
    room = ChallengeRoom.objects.filter(
        room_name=room_name, is_active=True)
    if room.exists():
        return JsonResponse({
            'success': True,
            'room_slug': room.first().room_slug,
            'room_name': room.first().room_name,
        })
    else:
        return JsonResponse({
            'success': False,
        })


def delete_room(request, slug):
    if ChallengeScore.objects.filter(room__room_slug=slug).exists():
        return JsonResponse({
            'success': False,
            'message': 'Room has been used'
        })
    else:
        get_object_or_404(ChallengeRoom, room_slug=slug).delete()
        return JsonResponse({
            'success': True,
            'message': 'Room has not been used'
        })


def get_challenge_questions(request, testid: int, limit: int):
    questions = []
    rounds = request.GET.get('rounds')

    for _ in range(int(rounds)):
        selected_questions = []
        all_questions = Question.objects.filter(quest__pk=testid).order_by('?')
        random_items = all_questions[:limit]
        for question in random_items:
            diagram_url = None
            if question.diagram:
                diagram_url = question.diagram.url
            selected_questions.append({
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
        else:
            questions.append(selected_questions)
    context = {
        'success': True,
        'questions': questions,
    }
    return JsonResponse(context)


def save_score(request):
    load_type = request.GET.get('type')
    if load_type == 'create':
        room_name = request.GET.get('room_name')
        username = request.GET.get('username')
        room = ChallengeRoom.objects.filter(
            room_name=room_name, is_active=True).first()
        user = get_object_or_404(User, username=username)
        score_instance = ChallengeScore()
        score_instance.room = room
        score_instance.user = user
        score_instance.save()
        return JsonResponse({'success': True})
    else:
        username = request.GET.get('username')
        room_slug = request.GET.get('room_name')
        score_1 = request.GET.get('score_1')
        score_2 = request.GET.get('score_2')
        score_3 = request.GET.get('score_3')
        score_4 = request.GET.get('score_4')
        score_5 = request.GET.get('score_5')
        room = ChallengeRoom.objects.get(room_slug=room_slug)
        room.is_active = False
        room.save()
        user_score = ChallengeScore.objects.get(
            user__username=username, room__pk=room.pk)
        user_score.score_1 = score_1
        user_score.score_2 = score_2
        user_score.score_3 = score_3
        user_score.score_4 = score_4
        user_score.score_5 = score_5
        user_score.save()
        return JsonResponse({'success': True})
