from django.contrib import admin

from qlab.apps.company.models import LabDevice, QualityMethod

# Register your models here.
admin.site.register(QualityMethod)
admin.site.register(LabDevice)
