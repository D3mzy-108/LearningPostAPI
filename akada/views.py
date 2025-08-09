from datetime import date
from decouple import config
from google import genai

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from admin_app.models import Quest
from admin_app.utils.grades import user_subscribed_grades
from akada.models import AkadaConversations, GeneratedStudyMaterials, GenerativeAIContentReport
from core.utils import send_email_to_recipient
from website.models import User
from endpoints.api_views.subscription import is_subscription_valid


def _send_request_to_ai(user: User | None, prompt: str) -> str | None:
    """
    This function sends a request to the connected AI model and returns a string response from the model
    """
    try:
        gemini_api_key = config('GEMINI_API_KEY')
        client = genai.Client(api_key=gemini_api_key)
        gemini_model = 'gemini-2.0-flash-lite'

        # CALCULATE USER AGE FOR TAILORED RESPONSE
        if user:
            today = date.today()
            dob = user.dob
            age = 10
            if dob:
                age = today.year - dob.year

            # FETCH RESPONSE FROM GEMINI AI
            user_prompt = f'{prompt}\n\nTailor the response for a {age} year old to easily understand'
        else:
            user_prompt = prompt
        response = client.models.generate_content(
            model=gemini_model,
            contents=[user_prompt],
        )
        return response.text
    except Exception as e:
        print(e)
        return None


@csrf_exempt
def prompt_akada(request, username: str):
    user = get_object_or_404(User, username=username)
    if not is_subscription_valid(user=user):
        return JsonResponse({
            'success': False,
            'message': 'Your subscription is expired!'
        })
    # GET LIST OF ALL PROMPTS SENT TO AKADA
    prompts = AkadaConversations.objects.filter(
        user__username=username).order_by('-id')
    prompts_list = []
    for p in prompts:
        prompts_list.append({
            'role': 'model',
            'parts': p.system_response,
        })
        prompts_list.append({
            'role': 'user',
            'parts': p.prompt,
        })
    conversation_context = 'Here are past responses as context:\n\n"'
    for pr in prompts_list[:4]:
        conversation_context += f'{pr["parts"]}\n'
    else:
        conversation_context += f'"\n\nRespond in an informal tone in about 150 words including as much detail as possible\n\n'
    if request.method == 'POST':
        try:
            # INIT GEMINI PARAMS
            prompt = request.POST.get('prompt')
            conversation_context += f'{prompt}'
            generated_text = _send_request_to_ai(
                user=user, prompt=conversation_context)
            akada_response = {
                'role': 'model',
                'parts': generated_text or '',
            }

            # SAVE PROMPT AND RESPONSE TO DATABASE
            user = User.objects.get(username=username)
            instance = AkadaConversations()
            instance.user = user
            instance.prompt = prompt
            instance.system_response = generated_text
            instance.save()
            prompts_list = [akada_response]
        except:
            prompts_list = [{
                'role': 'model',
                'parts': "🚨 Oops! Connection Trouble\nWe can't reach the AI server or knowledge base.\nCheck your internet and give it another try soon! 🔄🌐",
            }]

    return JsonResponse({
        'success': True,
        'prompts': prompts_list,
    })


@require_POST
@csrf_exempt
def request_smartlink(request, username: str):
    try:
        # VERIFY USER
        if not User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': 'Invalid user!',
            })
        # INIT GEMINI PARAMS
        user = User.objects.get(username=username)
        prompt = request.POST.get('prompt')
        generated_text = _send_request_to_ai(user=user,
                                             prompt=f'{prompt}\n\n Your response should be in about 200 words')
        akada_response = generated_text or ''
    except:
        akada_response = "🚨 Oops! Connection Trouble\nWe can't reach the AI server or knowledge base.\nCheck your internet and give it another try soon! 🔄🌐",
    return JsonResponse({
        'success': True,
        'smartlink_response': akada_response,
    })


def get_study_materials(request):
    search = request.GET.get('search') or ''
    uid = request.GET.get('uid') or ''
    user = get_object_or_404(User, username=uid)
    grades = user_subscribed_grades(user)
    if search == 'bookmarked':
        generated_study_materials = GeneratedStudyMaterials.objects.filter(
            bookmarked__pk=user.pk).order_by('topic')
        quests = None
    else:
        quests = Quest.objects.filter(
            title__icontains=search, organization=None).order_by('?')
        if len(grades) > 0:
            quests = quests.filter(grade__in=grades)
        generated_study_materials = GeneratedStudyMaterials.objects.filter(
            topic__icontains=search).order_by('topic')
    if len(grades) > 0:
        generated_study_materials = generated_study_materials.filter(
            quest__grade__in=grades)
    study_materials = [
        {
            'material_id': _.pk,
            'topic': _.topic,
            'cover_img': _.quest.cover.url if _.quest else None,
            'subject': _.quest.title if _.quest else None,
            'quest_id': _.quest.pk if _.quest else None,
            'bookmarked': _.bookmarked.filter(pk=user.pk).exists(),
        } for _ in generated_study_materials
    ]
    if quests:
        subjects_list = [
            {
                'cover': _.cover.url,
                'title': _.title,
                'description': _.about,
                'topics': [
                    {
                        'material_id': material.pk,
                        'topic': material.topic,
                        'quest_id': material.quest.pk if material.quest else None,
                        'bookmarked': material.bookmarked.filter(pk=user.pk).exists(),
                    } for material in generated_study_materials.filter(quest__pk=_.pk)
                ]
            } for _ in quests
        ]
    else:
        subjects_list = []
    return JsonResponse({
        'success': True,
        'study_materials': study_materials,
        'subjects': subjects_list,
    })


def get_material_content(request, material_id):
    generated_study_material = get_object_or_404(
        GeneratedStudyMaterials, pk=material_id)
    if not generated_study_material.content:
        akada_response = _send_request_to_ai(user=None,
                                             prompt=f'Write a short textbook covering all core areas on the topic "{generated_study_material.topic}" in 4000 words. Tailor response for a child in {generated_study_material.quest.grade} class or grade to easily understand.')
        if akada_response is None:
            print("FAILED TO GENERATE STUDY MATERIAL CONTENT")
            return JsonResponse({
                'success': False,
                'message': 'Unable to generate content. Please try again later.'
            })
        generated_study_material.content = akada_response
        generated_study_material.save()
    return JsonResponse({
        'success': True,
        'content': generated_study_material.content,
    })


def bookmark_study_material(request, material_id, username):
    try:
        generated_study_material = GeneratedStudyMaterials.objects.get(
            pk=material_id)
        user = User.objects.get(username=username)
        is_bookmarked = False
        if generated_study_material.bookmarked.filter(pk=user.pk).exists():
            generated_study_material.bookmarked.remove(user)
            is_bookmarked = False
        else:
            generated_study_material.bookmarked.add(user)
            is_bookmarked = True
        generated_study_material.save()
        return JsonResponse({
            'success': True,
            'message': 'Bookmark updated!',
            'bookmarked': is_bookmarked,
        })
    except:
        return JsonResponse({
            'success': False,
            'message': 'Item not found'
        })


@csrf_exempt
@require_POST
def flag_ai_response(request):
    # COLLECT POSTED DATA
    uid = request.POST.get('uid')
    prompt = request.POST.get('prompt')
    response = request.POST.get('response')
    reason = request.POST.get('reason')
    user = get_object_or_404(User, username=uid)
    
    report_instance = GenerativeAIContentReport()
    report_instance.reporter = user
    report_instance.prompt = prompt
    report_instance.response = response
    report_instance.reason = reason
    report_instance.save()
    
    send_email_to_recipient(
        recipient_email=user.email,
        email_content=f"""
        Hello {user.first_name},
        
        Thank you for reporting the AI-generated content. We've received your submission, and our team is actively reviewing it to address any concerns.
        
        
        At LearningPost, we take these reports seriously and are working hard to resolve all related issues. Our goal is to ensure a safe and enjoyable experience for all users.
        
        
        We appreciate your patience and support in helping us improve our platform. If you have any further questions, feel free to reach out.
        
        Best regards,
        Daniel Fisher
        LearningPost
        """,
        email_html_content=f"""
        <h2 style="color: #333333; font-size: 24px; margin-top: 0; margin-bottom: 15px;">
            Hello {user.first_name},
        </h2>
        <p style="margin-bottom: 15px;">
            Thank you for reporting the AI-generated content. We've received your submission, and our team is actively reviewing it to address any concerns.
        </p>
        <p style="margin-bottom: 15px;">
            At LearningPost, we take these reports seriously and are working hard to resolve all related issues. Our goal is to ensure a safe and enjoyable experience for all users.
        </p>
        <p style="margin-bottom: 15px;">
            We appreciate your patience and support in helping us improve our platform. If you have any further questions, feel free to reach out.
        </p>
        <p style="margin-bottom: 15px;">
            Best regards,
            <br/>
            Daniel Fisher
            <br/>
            LearningPost
        </p>
        """,
        subject="Your Report Has Been Received - LearningPost",
    )

    return JsonResponse({
        'success': True,
        'message': 'Our team has received your report and will review it shortly.',
    })
