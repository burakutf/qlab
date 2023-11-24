from django.contrib import admin

from qlab.apps.tenant.models import Domain, Organization

# Register your models here.
admin.site.register(Organization)
admin.site.register(Domain)