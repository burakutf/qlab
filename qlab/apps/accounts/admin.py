from django.contrib import admin

from qlab.apps.company.models import ProposalLogo

from .models import (
    Role,
    User,
    UserDetail,
)


admin.site.register(User)
admin.site.register(UserDetail)
admin.site.register(ProposalLogo)
admin.site.register(Role)
