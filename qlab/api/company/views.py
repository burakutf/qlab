from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.translation import gettext as _

from qlab.apps.accounts.models import User
from qlab.apps.company.models import (
    Company,
    LabDevice,
    MethodParameters,
    Proposal,
    ProposalDraft,
    QualityMethod,
    Vehicle,
)
from qlab.apps.core.models import Mediums, Notification
from .serializers import (
    LabDeviceSerializers,
    MethodParametersSerializers,
    MinimalQualityMethodSerializers,
    MinimalUserSerializers,
    NotificationSerializers,
    ProposalDraftSerializers,
    ProposalSerializers,
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
    search_fields = (
        'name',
        'contact_info',
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    search_fields = (
        'username',
        'full_name',
        'phone',
        'email',
    )


class NotificationView(
    mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = NotificationSerializers
    queryset = Notification.objects.none()

    def get_queryset(self):
        return (
            Notification.objects.filter(user=self.request.user)
            .filter(medium=Mediums.NOTIFICATION)
            .order_by('-created_at')
        )


class MinimalUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = MinimalUserSerializers
    search_fields = ('full_name',)


class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializers(user)
        return Response(serializer.data)


class QualityMethodViewSet(viewsets.ModelViewSet):
    queryset = QualityMethod.objects.all()
    serializer_class = QualityMethodSerializers
    search_fields = (
        'measurement_name',
        'measurement_number',
    )

    @action(detail=False, methods=['get'], url_path='minimal')
    def minimal(self, request):
        queryset = self.get_queryset()
        serializer = MinimalQualityMethodSerializers(queryset, many=True)
        return Response(serializer.data)


class MethodParametersViewSet(viewsets.ModelViewSet):
    queryset = MethodParameters.objects.all()
    serializer_class = MethodParametersSerializers
    search_fields = (
        'name',
        'method__measurement_name',
    )


class LabDeviceViewSet(viewsets.ModelViewSet):
    queryset = LabDevice.objects.all()
    serializer_class = LabDeviceSerializers
    search_fields = ('name',)


class ProposalDraftViewSet(viewsets.ModelViewSet):
    queryset = ProposalDraft.objects.all()
    serializer_class = ProposalDraftSerializers
    search_fields = ('title',)


class ProposalListCreateView(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializers
    filterset_fields = ('status',)
    search_fields = (
        'company__name',
        'draft__title',
    )


class ProposalRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializers

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
