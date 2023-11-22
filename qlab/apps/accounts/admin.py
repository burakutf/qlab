from django.contrib import admin

from qlab.apps.company.models import OrganizationInformation

from .models import (
    Role,
    User,
    UserDetail,
)


admin.site.register(User)
admin.site.register(UserDetail)
admin.site.register(OrganizationInformation)
admin.site.register(Role)
