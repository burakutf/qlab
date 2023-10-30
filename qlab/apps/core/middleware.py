from django.conf import settings
from django.http import HttpResponseForbidden
from django.db.models import Value, CharField
from django.db.models.functions import Concat

from qlab.apps.accounts.models import User


class TenantMediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_name = request.tenant.name
        settings.MEDIA_URL = f'/media/{tenant_name}/'

        response = self.get_response(request)

        return response


class UserPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if not request.META.get('PATH_INFO', '').startswith('/api/'):
            return self.get_response(request)

        if not user.is_authenticated:
            return self.get_response(request)

        user = User.objects.filter(id=user.id).first()
        if not user:
            return HttpResponseForbidden('User not found!')

        request.action_permissions = user.permissions + user.role.permissions

        return self.get_response(request)
