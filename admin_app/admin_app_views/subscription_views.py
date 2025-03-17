from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from admin_app.models import SubscriptionPlan


@login_required
def plans(request):
    plans = SubscriptionPlan.objects.all()
    context = {
        'plans': plans,
        'currencies': SubscriptionPlan.currencies,
    }
    return render(request, 'admin_app/subscription_plans/plans.html', context)


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
