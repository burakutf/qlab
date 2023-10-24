from django.conf import settings

class TenantMediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_name = request.tenant.name 
        settings.MEDIA_URL = f'/media/{tenant_name}/'

        response = self.get_response(request)

        return response
