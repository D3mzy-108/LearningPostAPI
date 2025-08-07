from admin_app.models import UserFeedback


def unread_report_count(request):
    feedbacks = UserFeedback.objects.all()
    h_count = feedbacks.filter(
        feedback_type='help_desk', status='pending').count()
    q_count = feedbacks.filter(
        feedback_type='question_report', status='pending').count()

    return {
        'h_count': h_count,
        'q_count': q_count,
        'ttl_unread_count': h_count + q_count,
    }
