from django.shortcuts import render, redirect, get_object_or_404

from admin_app.models import UserFeedback


def user_feedback(request):
    query = request.GET.get('q') or 'help_desk'
    selected_item = request.GET.get('selected') or ''
    feedbacks = UserFeedback.objects.filter(
        feedback_type=query).order_by('is_viewed', '-date', '-id')

    try:
        selected_feedback = UserFeedback.objects.get(pk=selected_item)
        selected_feedback.is_viewed = True
        selected_feedback.save()
    except:
        selected_feedback = None
    context = {
        'q': query,
        'selected_item': selected_item,
        'feedbacks': feedbacks,
        'selected_feedback': selected_feedback,
    }
    return render(request, 'admin_app/reports/user_reports.html', context)
