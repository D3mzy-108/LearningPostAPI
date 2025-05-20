import datetime
import json
from decouple import config
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
import requests
from admin_app.models import Quest, SubscriptionPlan
from admin_app.utils.grades import get_grades_list, set_user_subscribed_grades_string, user_subscribed_grades
from learningpost_professional.models import ProfessionalOrganization
from website.models import User, UserSubscription


def get_subscription_plans(request, username):
    subscription_plans = SubscriptionPlan.objects.all().order_by('duration')
    grades = get_grades_list()
    user_grades = user_subscribed_grades(
        get_object_or_404(User, username=username))
    grades_list = []
    for grade in grades:
        if Quest.objects.filter(grade=grade['grade'], organization=None).exists():
            grades_list.append(grade)
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
        'grades': grades_list,
        'user_grades': user_grades,
    })


@require_POST
@csrf_exempt
def make_subscription_request(request: HttpRequest):
    email = request.POST.get('email')
    plan_id = request.POST.get('plan_id')
    grades = request.POST.getlist('grades')
    if len(grades) == 0:
        return JsonResponse({
            'success': False,
            'message': 'Please select at least one grade, and ensure your app version is up to date.',
        })
    subscription_plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    user_subscription = UserSubscription.objects.get(profile__email=email)
    today = datetime.date.today()
    expiry_date = today + datetime.timedelta(days=subscription_plan.duration)
    user_subscription.expiry_date = expiry_date
    user_subscription.is_confirmed = False
    user_subscription.grades = set_user_subscribed_grades_string(grades)
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
        print(payload)
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
            print('USER NOT FOUND')
            return HttpResponse("User not found")

        # Get the user's wallet
        try:
            subscription = UserSubscription.objects.get(
                profile__email=user.email)
            subscription.is_confirmed = True
            subscription.save()

            # You can optionally return a success response to Flutterwave
            print('SUBSCRIPTION SUCCESSFUL')
            return HttpResponse("Subscription successful")
        except:
            print('SUBSCRIPTION FAILED')
            return HttpResponse("Subscription Failed")
    else:
        # Handle unsuccessful transactions (log or perform other actions)
        print('PAYMENT FAILED')
        return HttpResponse("Payment not successful")


def payment_success(request):
    return render(request, 'endpoints/successful_payment.html')


def is_subscription_valid(user: User) -> bool:
    try:
        today = datetime.date.today()
        subscription = UserSubscription.objects.get(
            profile__email=user.email, is_confirmed=True)
        target_date = subscription.expiry_date
        return target_date > today
    except:
        organizations = ProfessionalOrganization.objects.filter(
            members__pk=user.pk)
        return organizations.exists()
