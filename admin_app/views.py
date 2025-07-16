from django.http import JsonResponse

from admin_app.utils.grades import get_grades_list
from learningpost_professional.models import ProfessionalOrganization

def load_ext_form_data(request):
    grades = get_grades_list()
    organizations = ProfessionalOrganization.objects.all()
    context = {
        'success': True,
        'grades': grades,
        'organizations': [
            {
                'id': organization.pk,
                'name': organization.organization_name,
                'logo': organization.organization_logo.url,
                'code': organization.organization_code,
                } for organization in organizations
        ]
    }
    return JsonResponse(context)