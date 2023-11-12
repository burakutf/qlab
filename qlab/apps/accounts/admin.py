from django.contrib import admin

from .models import (
    Role,
    User,
    UserDetail,
)


admin.site.register(User)
admin.site.register(UserDetail)

admin.site.register(Role)
