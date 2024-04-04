from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def plans(request):
    context = {}
    return render(request, 'admin_app/subscription_plans/plans.html', context)
