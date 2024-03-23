from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from admin_app.models import Question, UserFeedback
from website.models import User
from django.views.decorators.csrf import csrf_exempt


def user_feedback(request):
    query = request.GET.get('q') or 'help_desk'
    selected_item = request.GET.get('selected') or ''
    feedbacks = UserFeedback.objects.filter(
        feedback_type=query).order_by('is_viewed', '-date', '-id')
    paginator = Paginator(feedbacks, 50)
    page = request.GET.get('page')
    if page == None or int(page) > paginator.num_pages:
        page = 1
    displayed_feeds = paginator.page(page)

    try:
        selected_feedback = UserFeedback.objects.get(pk=selected_item)
        selected_feedback.is_viewed = True
        selected_feedback.save()
        question = selected_feedback.question
    except:
        selected_feedback = None
        question = None
    context = {
        'q': query,
        'selected_item': selected_item,
        'selected_feedback': selected_feedback,
        'question': question,
        'feedbacks': displayed_feeds,
        'paginator': displayed_feeds,
        'page': page,
    }
    return render(request, 'admin_app/reports/user_reports.html', context)


@csrf_exempt
def send_report(request, username):
    if request.method == 'POST':
        questionid = request.POST.get('questionId') or ''
        report_type = request.POST.get('reportType')
        message = request.POST.get('message')
        feedback_instance = UserFeedback()
        report_type_is_valid = False
        for choice in feedback_instance.feedback_choices:
            if report_type == choice[0]:
                report_type_is_valid = True
        if report_type_is_valid:
            if questionid != '':
                feedback_instance.question = get_object_or_404(
                    Question, id=questionid)
            feedback_instance.feedback_type = report_type
            feedback_instance.message = message
            feedback_instance.user = get_object_or_404(User, username=username)
            feedback_instance.save()
            return JsonResponse({
                'success': True,
                'message': 'Report has been sent!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid report type!'
            })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request!'
        })
