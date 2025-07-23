from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from admin_app.models import SubscriptionPlan


def plans(request):
    plans = SubscriptionPlan.objects.all()
    context = {
        'success': True,
        'plans': [
            {
                'plan': plan.plan,
                'duration': plan.duration,
                'currency': plan.currency,
                'price': plan.price,
                'id': plan.pk,
            } for plan in plans
        ],
        'currencies': SubscriptionPlan.currencies,
    }
    # return render(request, 'admin_app/subscription_plans/plans.html', context)
    return JsonResponse(context)


@require_POST
@csrf_exempt
def save_plan_instance(request):
    if request.POST.get('id') is not None and not request.POST.get('id') == '':
        instance = get_object_or_404(SubscriptionPlan, id=request.POST.get('id'))
    else:
        instance = SubscriptionPlan()
    instance.plan = request.POST.get('plan')
    instance.duration = request.POST.get('duration')
    instance.currency = request.POST.get('currency')
    instance.price = request.POST.get('price')
    instance.save()
    return JsonResponse({
        'success': True,
        'message': 'Plan instance has been saved!',
    })


@login_required
def add_plan(request):
    if request.method == 'POST':
        plan = SubscriptionPlan()
        plan.plan = request.POST['plan']
        plan.duration = request.POST['duration']
        plan.currency = request.POST['currency']
        plan.price = request.POST['price']
        plan.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def modify_plan(request, id):
    if request.method == 'POST':
        plan = get_object_or_404(SubscriptionPlan, id=id)
        plan.plan = request.POST['plan']
        plan.duration = request.POST['duration']
        plan.currency = request.POST['currency']
        plan.price = request.POST['price']
        plan.save()
    return redirect(request.META.get('HTTP_REFERER'))
