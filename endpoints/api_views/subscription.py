from django.http import JsonResponse
from admin_app.models import SubscriptionPlan


def get_subscription_plans(request):
    subscription_plans = SubscriptionPlan.objects.all().order_by('duration')
    return JsonResponse({
        'success': True,
        'subscription_plans': [
            {
                'plan': plan.plan,
                'duration': plan.duration,
                'currency': plan.currency,
                'price': plan.price,
            } for plan in subscription_plans
        ],
    })
