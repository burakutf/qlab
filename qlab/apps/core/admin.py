from django.contrib import admin

from qlab.apps.core.models import AuthAttempt, Notification

# Register your models here.
admin.site.register(AuthAttempt)
admin.site.register(Notification)
