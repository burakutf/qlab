import logging

from rest_framework import serializers
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from qlab.apps.accounts.models import User

logger = logging.getLogger('AuthSerializer')


class PasswordField(serializers.CharField):
    def __init__(
        self,
        trim_whitespace=False,
        write_only=True,
        style={'input_type': 'password'},
        **kwargs,
    ):
        super().__init__(
            style=style,
            trim_whitespace=trim_whitespace,
            write_only=write_only,
            **kwargs,
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label='Username')
    password = PasswordField()
    token = serializers.CharField(label='Token', read_only=True)
    full_name = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not (username and password):
            msg = _('kullanıcı adı veya şifre gerekli.')
            raise serializers.ValidationError(msg, code='authorization')

        msg = _('Sağlanan kimlik bilgileriyle oturum açılamıyor.')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(msg, code='authorization')
        if not user.password == password:
            raise serializers.ValidationError(msg, code='authorization')
        attrs['full_name'] = user.full_name
        return attrs
