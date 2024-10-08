from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError

from django.shortcuts import get_object_or_404

from qlab.api.accounts.serializers import (
    GroupSerializer,
    MinimalUserSerializers,
    UserDetailSerializers,
    UserSerializers,
)
from qlab.apps.accounts.models import Role, User, UserDetail
from qlab.apps.accounts.permissions import PERMS_MAP, PermissionChoice


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializers
    search_fields = (
        'username',
        'full_name',
        'phone',
        'email',
    )
    action_permission_map = {
        'create': PermissionChoice.USER_CREATE,
        'update': PermissionChoice.USER_UPDATE,
        'destroy': PermissionChoice.USER_DELETE,
        'view': PermissionChoice.USER_VIEW,
    }

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            organization=user.organization, is_staff=False
        )


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = UserDetail.objects.none()
    serializer_class = UserDetailSerializers
    search_fields = ('user__full_name',)
    action_permission_map = {
        'create': PermissionChoice.USER_DETAIL_CREATE,
        'update': PermissionChoice.USER_DETAIL_UPDATE,
        'destroy': PermissionChoice.USER_DETAIL_DELETE,
        'view': PermissionChoice.USER_DETAIL_VIEW,
    }

    def get_queryset(self):
        user = self.request.user
        return UserDetail.objects.filter(user__organization=user.organization)


class MinimalUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.none()
    serializer_class = MinimalUserSerializers
    search_fields = ('full_name',)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(organization=user.organization)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.none()
    serializer_class = GroupSerializer
    search_fields = ('name',)
    action_permission_map = {
        'create': PermissionChoice.GROUP_CREATE,
        'update': PermissionChoice.GROUP_UPDATE,
        'destroy': PermissionChoice.GROUP_DELETE,
        'view': PermissionChoice.GROUP_VIEW,
    }

    def get_queryset(self):
        user = self.request.user
        queryset = Role.objects.filter(
            organization=user.organization, is_primary=False
        )
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except ProtectedError:
            return Response(
                {
                    'message': 'Bu rol bir kullanıcıya atanmış olduğu için silinemez.'
                },
                status=400,
            )
        return Response(status=204)


class PermissionView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(PERMS_MAP)


class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializers(user)
        return Response(serializer.data)
