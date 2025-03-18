import datetime
import json
from decouple import config
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
import requests
from admin_app.models import SubscriptionPlan
from website.models import User, UserSubscription


def get_subscription_plans(request):
    subscription_plans = SubscriptionPlan.objects.all().order_by('duration')
    return JsonResponse({
        'success': True,
        'subscription_plans': [
            {
                'id': plan.pk,
                'plan': plan.plan,
                'duration': plan.duration,
                'currency': plan.currency,
                'price': plan.price,
            } for plan in subscription_plans
        ],
    })


@require_POST
@csrf_exempt
def make_subscription_request(request):
    email = request.POST.get('email')
    plan_id = request.POST.get('plan_id')
    subscription_plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    user_subscription = UserSubscription.objects.get(profile__email=email)
    today = datetime.date.today()
    expiry_date = today + datetime.timedelta(days=subscription_plan.duration)
    user_subscription.expiry_date = expiry_date
    user_subscription.is_confirmed = False
    user_subscription.save()
    return JsonResponse({
        'success': True,
        'message': 'Subscription request sent successfully',
    })


@require_http_methods(["GET", "POST"])
@csrf_exempt
def subscribe(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
        transaction_id = payload['id']
    except Exception as e:
        return HttpResponse(f"Error parsing payload: {e}")

    req = requests.get(
        f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify",
        headers={
            'Authorization': f'Bearer {config("FLUTTERWAVE_SECRET_KEY")}'
        }
    )
    if not req.ok:
        # print(req.json())
        return HttpResponse("Invalid request data")

    data = req.json()['data']

    if data['status'] == 'successful':
        customer_email = data['customer']['email']

        # Get the user object using the email
        try:
            user = User.objects.get(email=customer_email)
        except User.DoesNotExist:
            return HttpResponse("User not found")

        # Get the user's wallet
        try:
            subscription = UserSubscription.objects.get(
                profile__email=user.email)
            subscription.is_confirmed = True
            subscription.save()

            # You can optionally return a success response to Flutterwave
            return HttpResponse("Subscription successful")
        except:
            return HttpResponse("Subscription Failed")
    else:
        # Handle unsuccessful transactions (log or perform other actions)
        return HttpResponse("Payment not successful")


def payment_success(request):
    return render(request, 'endpoints/successful_payment.html')


def is_subscription_valid(user: User) -> bool:
    today = datetime.date.today()
    subscription = UserSubscription.objects.get(
        profile__email=user.email)
    target_date = subscription.expiry_date
    return target_date > today
