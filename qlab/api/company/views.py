from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils.translation import gettext as _

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
    NotificationSerializers,
    ProposalDraftSerializers,
    ProposalSerializers,
    QualityMethodSerializers,
    CompanySerializers,
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

    @action(detail=False, methods=['get'], url_path='minimal')
    def minimal(self, request):
        queryset = self.get_queryset().values('id', 'name')
        return Response(list(queryset))


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


class QualityMethodViewSet(viewsets.ModelViewSet):
    queryset = QualityMethod.objects.all()
    serializer_class = QualityMethodSerializers
    search_fields = (
        'measurement_name',
        'measurement_number',
    )

    @action(detail=False, methods=['get'], url_path='minimal')
    def minimal(self, request):
        queryset = self.get_queryset().values('id', 'measurement_number')
        return Response(list(queryset))


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

    @action(detail=False, methods=['get'], url_path='minimal')
    def minimal(self, request):
        queryset = self.get_queryset().values('id', 'title')
        return Response(list(queryset))


class ProposalListCreateView(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializers
    ordering_fields = ('-created_at',)
    filterset_fields = ('status','user',)
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
