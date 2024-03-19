import string
import random
from django.shortcuts import render, redirect, get_object_or_404
from website.models import BetaReferal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# ========================================================================================================
# CLASSIFICATIONS
# ========================================================================================================

@login_required
def classifications(request):
    referrals = BetaReferal.objects.all().order_by('-id')
    paginator = Paginator(referrals, 50)
    page = request.GET.get('page')
    if page == None or int(page) > paginator.num_pages:
        page = 1
    displayed_refs = paginator.page(page)
    context = {
        'referrals': displayed_refs,
        'paginator': displayed_refs,
        'page': page,
    }
    return render(request, 'admin_app/classifications/classifications.html', context)


@login_required
def generate_new_code(request):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(15))
    if not BetaReferal.objects.filter(code=random_string).exists():
        referal = BetaReferal()
        referal.code = random_string
        referal.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_code(request, id):
    referral = get_object_or_404(BetaReferal, id=id)
    profile = referral.profile
    if profile is not None:
        profile.delete()
    referral.delete()
    return redirect(request.META.get('HTTP_REFERER'))
