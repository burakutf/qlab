from rest_framework import viewsets

from django.utils.translation import gettext as _

from qlab.apps.accounts.models import Company, User, Vehicle
from qlab.apps.company.models import LabDevice, QualityMethod
from .serializers import (
    LabDeviceSerializers,
    QualityMethodSerializers,
    CompanySerializers,
    UserSerializers,
    VehicleSerializers,
)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    search_fields = (
        'brand',
        'model',
        'plate',
    )

    def get_queryset(self):
        fullness = self.request.query_params.get('fullness', None)
        if fullness is not None:
            return Vehicle.objects.filter(user__isnull=fullness)
        return Vehicle.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializers
    search_fields = ('name', 'contact_info')


# TODO Buralara sadece staff erişebilir olmalı permiison class yaz
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    search_fields = ('username', 'full_name', 'phone', 'email')


# TODO Daha sonra burayı apiview yapmayı düşünebilirsin
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializers

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class QualityMethodViewSet(viewsets.ModelViewSet):
    queryset = QualityMethod.objects.all()
    serializer_class = QualityMethodSerializers
    search_fields = ('measurement_name', 'measurement_number')


class LabDeviceViewSet(viewsets.ModelViewSet):
    queryset = LabDevice.objects.all()
    serializer_class = LabDeviceSerializers
    search_fields = ('name',)
