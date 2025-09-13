import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from learningpost_professional.models import ProfessionalOrganization, Test, TestAttempt, TestQuestion
from website.models import User

def certification_test_list(request, username):
    """
    Displays a list of all available tests to the logged-in user.
    """
    user = get_object_or_404(User, username=username)
    organization_code = request.GET.get('code') or None
    if organization_code is None or organization_code == '':
        return JsonResponse({
            'success': False,
            'message': 'Track not found!',
        })
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk, organization_code=organization_code)
    tests = Test.objects.filter(organization__in=organizations)
    tests_list = [{
        'testid': test.pk,
        'title': test.title,
        'cover': test.cover.url,
        'time': test.time,
        'about': test.about,
        'instructions': test.instructions,
        'is_locked': test.expires <= datetime.date.today(),
        'is_attempted': test.attempts.all().filter(user__username=username).exists(),
        'status': 'Closed' if test.expires <= datetime.date.today() else f'Closes on {test.expires}',
        'question_count': test.test_questions.count(),
    } for test in tests]

    return JsonResponse({
        'success': True,
        'tests': tests_list,
    })

def start_test(request, username, test_id):
    """
    Initiates an test attempt for the user.
    If an active attempt exists for this test, it resumes it.
    """
    test = get_object_or_404(Test, id=test_id)

    # Check for existing active attempt (not ended, not voided)
    active_attempt = TestAttempt.objects.filter(user__username=username, test__id=test_id)

    if active_attempt.exists():
        return JsonResponse({
            'success': False,
            'message': 'You have already attempted this test!'
        })
    
    attempt = TestAttempt(
        user=get_object_or_404(User, username=username),
        test=test,
    )
    attempt.save()
    
    questions = TestQuestion.objects.filter(test__pk=test_id).order_by('?')[:100]
    questions_list = []
    for question in questions:
        diagram_url = None
        if question.diagram:
            diagram_url = question.diagram.url
        questions_list.append({
            'testid': question.test.pk,
            'comprehension': question.comprehension,
            'diagram': diagram_url,
            'question': question.question,
            'a': question.a,
            'b': question.b,
            'c': question.c,
            'd': question.d,
            'answer': question.answer,
        })
    return JsonResponse({
        'success': True,
        'questions': questions_list,
    })


@require_POST
@csrf_exempt
def save_test_score(request, username: str, testid: int):
    try:
        score = request.POST.get('score')
        score_val = float(f'{score:.2f}')
        attempts = TestAttempt.objects.filter(
            test__pk=testid, user__username=username)
        if attempts.exists():
            attempt = attempts.first()
            attempt.score = score_val
            attempt.is_attempted = True
            attempt.save()
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid information provided',
            })
        return JsonResponse({
            'success': True,
            'message': 'Score has been saved!',
        })
    except:
        return JsonResponse({
            'success': False,
            'message': 'Invalid information provided',
        })


def get_attempt(request, username: str, testid: int):
    user = get_object_or_404(User, username=username)
    # organizations = ProfessionalOrganization.objects.filter(
    #     members__pk=user.pk)
    attempt = TestAttempt.objects.filter(
        test__pk=testid, user=user).first()
    if attempt is not None:
        return JsonResponse({
            'success': True,
            'attempt': attempt.to_json()
        })
    else:
        return JsonResponse({
            'success': False,
            'message': "Couldn't find record of user's attempt"
        })

# @login_required
# def submit_proctoring_event(request, attempt_id):
#     """
#     API endpoint to receive and log proctoring events from the frontend.
#     Updates the attempt's proctoring failure count and voids test if necessary.
#     """
#     if request.method == 'POST':
#         attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)

#         # Do not process events if test is already voided or finished
#         if attempt.is_voided or attempt.end_time:
#             return JsonResponse({'status': 'ignored', 'message': 'Exam already voided or finished.'})

#         try:
#             data = json.loads(request.body)
#             event_type = data.get('event_type')
#             details = data.get('details')

#             # Only increment failures for actual violation events
#             if event_type in ['LOOK_AWAY', 'UNRECOGNIZED_FACE', 'TAB_SWITCH', 'FULLSCREEN_EXIT', 'RECOGNITION_FAILURE', 'LOW_ATTENTION']:
#                 attempt.proctoring_failures += 1
#                 if attempt.proctoring_failures >= 3: # Threshold for voiding test
#                     attempt.is_voided = True
#                     ProctoringLog.objects.create(
#                         attempt=attempt, event_type='EXAM_VOIDED',
#                         details=f"Exam voided automatically due to {attempt.proctoring_failures} accumulated proctoring failures."
#                     )
#                 attempt.save() # Save the updated failure count or void status

#             # Log all proctoring events for auditing
#             ProctoringLog.objects.create(
#                 attempt=attempt,
#                 event_type=event_type,
#                 details=details
#             )
#             return JsonResponse({
#                 'status': 'success',
#                 'proctoring_failures': attempt.proctoring_failures,
#                 'is_voided': attempt.is_voided
#             })
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON in request body'}, status=400)
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#     return HttpResponseForbidden() # Only allow POST requests
