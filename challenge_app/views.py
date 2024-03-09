from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from admin_app.models import Question
from challenge_app.models import ChallengeRoom, ChallengeScore


def create_room(request):
    room_name = request.GET.get('room_name')
    # CREATE ROOM INSTANCE
    room_instance = ChallengeRoom()
    room_instance.room_name = room_name
    room_instance.save()
    return JsonResponse({
        'success': True,
        'room_slug': room_instance.room_slug,
        'room_name': room_instance.room_name,
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


def get_challenge_questions(request, testid, limit):
    all_questions = Question.objects.filter(quest__pk=testid).order_by('?')
    random_items = all_questions[:limit]
    selected_questions = []

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
    context = {
        'success': True,
        'questions': selected_questions,
    }
    return JsonResponse(context)
