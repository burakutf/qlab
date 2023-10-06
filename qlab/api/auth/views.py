from rest_framework import views

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.utils.translation import gettext as _
from django.contrib.auth.models import update_last_login

from qlab.apps.accounts.models import User
from ..utils.permissions import CanAttemptPerm
from .serializers import (
    LoginSerializer,
)


class LoginView(views.APIView):
    permission_classes = [AllowAny, CanAttemptPerm]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=400)
        user = User.objects.get(username=serializer.data['username'])
        if not user.is_active:
            return Response(
                data={'detail': _('Hesabınız aktif değil!')}, status=403
            )

        token, x = Token.objects.get_or_create(user=user)
        update_last_login(None, user)

        return Response(data={'token': str(token)})
