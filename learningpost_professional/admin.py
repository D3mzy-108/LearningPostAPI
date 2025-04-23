from django.contrib import admin

from learningpost_professional.models import ProfessionalOrganization


@admin.register(ProfessionalOrganization)
class ProfessionalOrganizationAdmin(admin.ModelAdmin):
    pass
    # list_display = ('',)
    # list_filter = ('',)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
