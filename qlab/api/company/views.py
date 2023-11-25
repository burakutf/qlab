from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from django.utils.translation import gettext as _
from qlab.apps.accounts.permissions import PermissionChoice

from qlab.apps.company.models import (
    Company,
    CompanyNote,
    LabDevice,
    MethodParameters,
    OrganizationInformation,
    Proposal,
    ProposalDraft,
    QualityMethod,
    Vehicle,
    WorkOrder,
)
from qlab.apps.core.models import Mediums, Notification
from qlab.apps.core.utils.send_email import (
    general_html_content,
    send_html_mail,
)
from .serializers import (
    CompanyNoteSerializers,
    LabDeviceSerializers,
    MethodParametersSerializers,
    NotificationSerializers,
    OrganizationInformationSerializers,
    ProposalDraftSerializers,
    ProposalSerializers,
    QualityMethodSerializers,
    CompanySerializers,
    VehicleSerializers,
    WorkOrderSerializers,
)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    search_fields = (
        'brand',
        'model',
        'plate',
    )
    action_permission_map = {
        'create': PermissionChoice.VEHICLE_CREATE,
        'update': PermissionChoice.VEHICLE_UPDATE,
        'destroy': PermissionChoice.VEHICLE_DELETE,
        'view': PermissionChoice.VEHICLE_VIEW,
    }

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
    action_permission_map = {
        'create': PermissionChoice.COMPANY_CREATE,
        'update': PermissionChoice.COMPANY_UPDATE,
        'destroy': PermissionChoice.COMPANY_DELETE,
        'view': PermissionChoice.COMPANY_VIEW,
    }

    @action(detail=False, methods=['get'], url_path='minimal')
    def minimal(self, request):
        queryset = self.get_queryset().values('id', 'name')
        return Response(list(queryset))


class NotificationView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
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
    action_permission_map = {
        'create': PermissionChoice.METHOD_CREATE,
        'update': PermissionChoice.METHOD_UPDATE,
        'destroy': PermissionChoice.METHOD_DELETE,
        'view': PermissionChoice.METHOD_VIEW,
    }

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
    action_permission_map = {
        'create': PermissionChoice.PARAMETER_CREATE,
        'update': PermissionChoice.PARAMETER_UPDATE,
        'destroy': PermissionChoice.PARAMETER_DELETE,
        'view': PermissionChoice.PARAMETER_VIEW,
    }


class LabDeviceViewSet(viewsets.ModelViewSet):
    queryset = LabDevice.objects.all()
    serializer_class = LabDeviceSerializers
    search_fields = ('name',)
    action_permission_map = {
        'create': PermissionChoice.DEVICE_CREATE,
        'update': PermissionChoice.DEVICE_UPDATE,
        'destroy': PermissionChoice.DEVICE_DELETE,
        'view': PermissionChoice.DEVICE_VIEW,
    }


class ProposalDraftViewSet(viewsets.ModelViewSet):
    queryset = ProposalDraft.objects.all()
    serializer_class = ProposalDraftSerializers
    search_fields = ('title',)
    action_permission_map = {
        'create': PermissionChoice.DRAFT_CREATE,
        'update': PermissionChoice.DRAFT_UPDATE,
        'destroy': PermissionChoice.DRAFT_DELETE,
        'view': PermissionChoice.DRAFT_VIEW,
    }

    @action(detail=False, methods=['get'], url_path='minimal')
    def minimal(self, request):
        queryset = self.get_queryset().values('id', 'title')
        return Response(list(queryset))


class OrganizationInformationViewSet(viewsets.ModelViewSet):
    queryset = OrganizationInformation.objects.all()
    serializer_class = OrganizationInformationSerializers
    action_permission_map = {
        'create': PermissionChoice.ORG_INFO_CREATE,
        'update': PermissionChoice.ORG_INFO_UPDATE,
        'destroy': PermissionChoice.ORG_INFO_DELETE,
        'view': PermissionChoice.ORG_INFO_VIEW,
    }


class ProposalListCreateView(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializers
    filterset_fields = (
        'status',
        'user',
    )
    search_fields = (
        'company__name',
        'draft__title',
    )

    def get_permissions(self):
        has_perm = (
            PermissionChoice.PROPOSAL_VIEW in self.request.action_permissions
        )
        if not has_perm:
            raise PermissionDenied('Teklif görüntüleme yetkiniz yok!')
        return super().get_permissions()


class ProposalRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializers

    def patch(self, request, *args, **kwargs):
        has_perm = (
            PermissionChoice.PROPOSAL_UPDATE in self.request.action_permissions
        )
        if not has_perm:
            raise PermissionDenied(('Teklif Güncelleme yetkiniz yok!'))
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        status = request.data.get('status')
        if int(status) == 2:
            note = request.data.get('note')
            company_name = instance.company.name
            user = instance.user
            rejection_title = f'{company_name} Şirketine Hazırladığınız Teklif Yöneticiniz Tarafından Reddedilmiştir'
            Notification.objects.create(
                user=user, title=rejection_title, text=note
            )
            send_html_mail(
                subject='Qlab Teklif Durumu',
                recipient_list=(user.email,),
                html_content=general_html_content(
                    name=user.full_name,
                    title=rejection_title,
                    text=f'Reddedilme Nedeni: <br/>{note}',
                ),
            )

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CompanyNoteViewSet(viewsets.ModelViewSet):
    queryset = CompanyNote.objects.all()
    serializer_class = CompanyNoteSerializers
    action_permission_map = {
        'create': PermissionChoice.NOTE_CREATE,
        'update': PermissionChoice.NOTE_UPDATE,
        'destroy': PermissionChoice.NOTE_DELETE,
        'view': PermissionChoice.NOTE_VIEW,
    }

    def create(self, request, *args, **kwargs):
        date = request.data.get('date')
        note_exists = CompanyNote.objects.filter(date=date).first()

        if note_exists:
            serializer = self.get_serializer(note_exists, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        return super().create(request, *args, **kwargs)


class WorkOrderView(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializers
    action_permission_map = {
        'create': PermissionChoice.WORK_ORDER_CREATE,
        'update': PermissionChoice.WORK_ORDER_UPDATE,
        'destroy': PermissionChoice.WORK_ORDER_DELETE,
        'view': PermissionChoice.WORK_ORDER_VIEW,
    }
