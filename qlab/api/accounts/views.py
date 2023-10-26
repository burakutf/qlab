from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404

from qlab.api.accounts.serializers import (
    GroupSerializer,
    MinimalUserSerializers,
    PermissionSerializer,
    UserSerializers,
)
from qlab.apps.accounts.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    search_fields = (
        'username',
        'full_name',
        'phone',
        'email',
    )


class MinimalUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = MinimalUserSerializers
    search_fields = ('full_name',)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializers(user)
        return Response(serializer.data)
