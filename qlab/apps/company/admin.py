from django.contrib import admin
from qlab.apps.company.models import (
    LabDevice,
    QualityMethod,
    Company,
    Vehicle,
    MethodParameters,
    ProposalDraft,
    Proposal,
    ProposalMethodParameters,
)

admin.site.register(QualityMethod)
admin.site.register(LabDevice)
admin.site.register(Company)
admin.site.register(Vehicle)
admin.site.register(MethodParameters)
admin.site.register(ProposalDraft)
admin.site.register(Proposal)
admin.site.register(ProposalMethodParameters)
