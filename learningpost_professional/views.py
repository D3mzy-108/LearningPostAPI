from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from admin_app.models import Quest
from endpoints.api_views.quest_views import _build_quest_object
from learningpost_professional.models import ProfessionalOrganization
from website.models import User


def pro_quests(request, username):
    user = get_object_or_404(User, username=username)
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk)
    quests = Quest.objects.filter(organization__in=organizations).order_by('?')

    search = request.GET.get('search')
    if search is not None:
        quests = quests.filter(
            title__icontains=search)
    quests_list = []
    for quest in quests:
        quests_list.append(_build_quest_object(quest, username))
    context = {
        'success': True,
        'quests': quests_list,
    }
    return JsonResponse(context)
