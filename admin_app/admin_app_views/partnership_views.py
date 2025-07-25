from django.http import JsonResponse
from learningpost_professional.models import ProfessionalOrganization


def get_partners(request):
    partners = ProfessionalOrganization.objects.all().order_by('-id')
    return JsonResponse({
        'success': True,
        'partners': [
            {
                'id': partner.pk,
                'name': partner.organization_name,
                'logo': partner.organization_logo.url,
                'code': partner.organization_code,
            } for partner in partners
        ],
    })
