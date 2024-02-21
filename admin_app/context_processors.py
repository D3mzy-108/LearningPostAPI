from admin_app.models import UserFeedback


def unread_report_count(request):
    feedbacks = UserFeedback.objects.all()
    h_count = feedbacks.filter(
        feedback_type='help_desk', is_viewed=False).count()
    q_count = feedbacks.filter(
        feedback_type='question_report', is_viewed=False).count()

    return {
        'h_count': h_count,
        'q_count': q_count,
        'ttl_unread_count': h_count + q_count,
    }
