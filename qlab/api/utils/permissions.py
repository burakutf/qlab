from datetime import timedelta

from django.utils import timezone
from django.db.models import Q
from django.conf import settings

from rest_framework.permissions import BasePermission, SAFE_METHODS

from ipware import get_client_ip
from qlab.apps.core.models import AuthAttempt
from qlab.apps.accounts.permissions import PERMS_MAP


class CanAttemptPerm(BasePermission):
    message = (
        'Çok fazla denemede bulundunuz! Bir kaç saat sonra tekrar deneyin!'
    )

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or not settings.ATTEMPT_PROTECTION:
            return True

        ip, is_routable = get_client_ip(request)

        if (ip is None or not is_routable) and not settings.DEVELOPMENT_MODE:
            self.message = 'Ip adresiniz ile ilgili bir sorun oluştu!'
            return False
        username = request.data.get('username', None)
        a_hour_ago = timezone.now() - timedelta(hours=1)

        total_attempts_in_last_hour = (
            AuthAttempt.objects.filter(
                Q(ip=ip) | Q(username=username), time__gt=a_hour_ago
            )
            .distinct()
            .count()
        )
        if (
            total_attempts_in_last_hour >= 300
        ):   # TODO ürün aşamasında 20 ile sınırla
            return False

        AuthAttempt.objects.create(username=username, ip=ip)
        return True


class ActionPermission(BasePermission):
    default_permission_map = {
        'get': 'app.view_model',
        'post': 'app.add_model',
        'put': 'app.change_model',
        'delete': 'app.delete_model',
    }

    def has_permission(self, request, view):
        action = self._get_action(view)
        action_permission_map = getattr(
            view, 'action_permission_map', self.default_permission_map
        )
        required_permission = action_permission_map.get(action)
        if not required_permission:
            return True
        self.message = f'Bu işlem için "{required_permission.lower()}" izninizin olması gerekir.'
        return required_permission in request.action_permissions

    def _get_action(self, view):
        action = getattr(view, 'action', 'default')
        if action in ['retrieve', 'list']:
            action = 'view'
        if action == 'partial_update':
            action = 'update'
        return action
