from django.conf import settings


from re import sub
from rest_framework.authtoken.models import Token


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

    def set_permissions(self, request):
        user = request.user
        if not request.META.get('PATH_INFO', '').startswith('/api/'):
            return self.get_response(request)

        if not user.is_authenticated:
            return self.get_response(request)

        permissions = []
        if hasattr(user, 'role.permissions'):
            permissions = user.role.permissions
        request.action_permissions = user.permissions + permissions

    def __call__(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            try:
                token = sub('Token ', '', header_token)
                token_obj = Token.objects.get(key=token)
                request.user = token_obj.user
                self.set_permissions(request)
            except Token.DoesNotExist:
                pass
        #TODO BU kısımı swagger için yaptım ama sonradan kaldırılanabilinir hacky yöntem gibi geliyor
        if request.user:
            self.set_permissions(request)

        return self.get_response(request)
