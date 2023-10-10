from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from django.utils.translation import gettext as _

from qlab.apps.accounts.models import Company, User, Vehicle
from .serializers import (
    CompanySerializers,
    UserSerializers,
    VehicleSerializers,
)

# TODO Searchlar genel olacak sadece nameye göre değil
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    filter_backends = (SearchFilter,)
    search_fields = (
        'brand',
        'model',
        'plate',
    )


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializers
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'contact_info')


# TODO Buralara sadece staff erişebilir olmalı permiison class yaz
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'full_name', 'phone', 'email')


# TODO Daha sonra burayı apiview yapmayı düşünebilirsin
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializers

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)
