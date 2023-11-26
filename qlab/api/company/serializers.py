from uuid import uuid4
from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from django.utils import timezone
from django.db import transaction
from qlab.apps.accounts.permissions import PermissionChoice

from qlab.apps.company.models import (
    Company,
    CompanyNote,
    LabDevice,
    MethodParameters,
    OrganizationInformation,
    Proposal,
    ProposalDraft,
    ProposalMethodParameters,
    QualityMethod,
    Vehicle,
    WorkOrder,
)
from qlab.apps.core.models import Notification
from qlab.apps.core.utils.offers_pdf_creater.invoice import InvoiceGenerator
from qlab.apps.core.utils.offers_pdf_creater.work_order import (
    WorkOrderGenerator,
)


class VehicleSerializers(serializers.ModelSerializer):
    users_full_names = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = '__all__'

    def get_users_full_names(self, obj):
        return [user.full_name for user in obj.user.all() if user.full_name]


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class QualityMethodSerializers(serializers.ModelSerializer):
    class Meta:
        model = QualityMethod
        fields = '__all__'


class CompanyNoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyNote
        fields = '__all__'


class MethodParametersSerializers(serializers.ModelSerializer):
    method_names = serializers.SerializerMethodField()
    method_data = serializers.SerializerMethodField()

    class Meta:
        model = MethodParameters
        fields = '__all__'

    def get_method_names(self, obj):
        method_names = [
            method.measurement_number for method in obj.method.all()
        ]
        return method_names

    def get_method_data(self, obj):
        method_data = [
            {'id': method.id, 'measurement_number': method.measurement_number}
            for method in obj.method.all()
        ]
        return method_data


class LabDeviceSerializers(serializers.ModelSerializer):
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = LabDevice
        fields = '__all__'

    def get_remaining_days(self, obj):
        if obj.finish_date:
            return (obj.finish_date - timezone.now().date()).days
        return 0

    def update(self, instance, validated_data):
        # Eğer start_date veya period güncellendi ise, finish_date'i tekrar hesapla
        if 'start_date' in validated_data or 'period' in validated_data:
            start_date = validated_data.get('start_date', instance.start_date)
            period = validated_data.get('period', instance.period)
            validated_data['finish_date'] = start_date + timezone.timedelta(
                days=period
            )

        return super().update(instance, validated_data)


class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ('user', 'medium')


class ProposalDraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProposalDraft
        fields = '__all__'


class OrganizationInformationSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrganizationInformation
        fields = '__all__'


class WorkOrderSerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source='proposal.company.name', read_only=True
    )
    company_address = serializers.CharField(
        source='proposal.company.address', read_only=True
    )
    company_authorized_person = serializers.CharField(
        source='proposal.company.authorized_person', read_only=True
    )  # TODO kullanılmazsa kaldır altakiyle bunu
    company_advisor = serializers.CharField(
        source='proposal.company.advisor', read_only=True
    )

    class Meta:
        model = WorkOrder
        fields = '__all__'

    def create(self, validated_data):
        vehicles = validated_data['vehicles']
        devices = validated_data['devices']
        proposal = validated_data['proposal']
        personal = validated_data['personal']
        vehicles_name = [i.plate for i in vehicles]
        vehicles_name_str = ', '.join(vehicles_name)
        personal_name = [i.full_name for i in personal]
        personal_name_str = ', '.join(personal_name)
        lab_devices = [
            {
                'id': i.id,
                'name': i.name,
                'serial_number': i.serial_number,
            }
            for i in devices
        ]
        items = [
            {
                'id': i.id,
                'price': i.price,
                'methods': i.methods,
                'count': i.count,
                'parameter': i.parameter.name,
            }
            for i in proposal.parameters.all()
        ]
        org_info = OrganizationInformation.objects.first()
        work_order_pdf = WorkOrderGenerator(
            proposal_id=proposal.id,
            items=items,
            org_owner=org_info.owner,
            signature=org_info.signature,
            left_logo=org_info.left_logo,
            devices=lab_devices,
            company_name=proposal.company.name,
            company_address=proposal.company.address,
            company_advisor=proposal.company.advisor,
            company_person=proposal.company.authorized_person,
            company_number=proposal.company.contact_info,
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date'],
            goal=validated_data['goal'],
            vehicles=vehicles_name_str,
            personal=personal_name_str,
        )
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'{str(uuid4())[:8]}_{timestamp}.pdf'
        work_order_object = super().create(validated_data)

        work_order_pdf.generate_pdf(filename)

        work_order_object.file = f'/{filename}'
        work_order_object.save()
        return work_order_object


class ParametersSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='parameter.id')
    count = serializers.IntegerField()
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    methods = serializers.ListField()
    parameter_name = serializers.CharField(source='parameter.name',read_only=True)
    parameter_id = serializers.IntegerField(source='id')

class ProposalSerializers(serializers.ModelSerializer):
    parameters = ParametersSerializer(many=True, required=False)
    company_name = serializers.CharField(source='company.name', read_only=True)
    user_full_name = serializers.CharField(
        source='user.full_name', read_only=True
    )
    draft_name = serializers.CharField(source='draft.title', read_only=True)

    class Meta:
        model = Proposal
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        has_perm = (
            PermissionChoice.PROPOSAL_CREATE in request.action_permissions
        )
        if not has_perm:
            raise PermissionDenied(('Teklif oluşturma yetkiniz yok!'))

        parameters_data = validated_data.pop('parameters', None)
        proposal_object = Proposal.objects.create(**validated_data)
        proposal_method_parameters = []
        items = []
        for parameter_data in parameters_data:
            try:
                parameter = MethodParameters.objects.get(
                    id=parameter_data['parameter']['id']
                )
            except MethodParameters.DoesNotExist:
                raise serializers.ValidationError(
                    {'error': ['Parametre bulunamadı!']}
                )

            method_names = [name for name in parameter_data['methods']]
            measurement_name = ', '.join(method_names)
            items.append(
                {
                    'name': parameter.name,
                    'description': measurement_name,
                    'unit_price': parameter_data['price'],
                    'quantity': parameter_data['count'],
                }
            )
            proposal_method_parameter = ProposalMethodParameters(
                proposal=proposal_object,
                parameter=parameter,
                count=parameter_data['count'],
                price=parameter_data['price'],
                methods=method_names,
            )
            proposal_method_parameter.save()

        with transaction.atomic():
            ProposalMethodParameters.objects.bulk_create(
                proposal_method_parameters
            )
        user = request.user
        org_info = OrganizationInformation.objects.first()

        invoice_generator = InvoiceGenerator(
            (user.full_name).upper(),
            items,
            8,
            proposal_object.draft.preface,
            proposal_object.draft.terms,
            org_info.owner,
            org_info.name,
            org_info.address,
            org_info.phone,
            org_info.mail,
            org_info.left_logo,
            org_info.right_logo,
            org_info.signature,
            org_info.bank_name,
            org_info.bank_no,
            org_info.bank_branch,
            org_info.bank_iban,
            proposal_object.company.name,
            proposal_object.company.address,
            proposal_object.company.authorized_person,
            proposal_object.company.contact_info,
            proposal_object.company.contact_info_mail,
            proposal_object.draft.title,
        )

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'{str(uuid4())[:8]}_{timestamp}.pdf'
        try:
            invoice_generator.generate_pdf(filename)
        except:
            raise serializers.ValidationError(
                {'error': ['Pdf Oluşturulamadı!']}
            )
        proposal_object.user = user
        proposal_object.file = f'/{filename}'
        proposal_object.save()
        return proposal_object
