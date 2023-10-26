import os
from uuid import uuid4
from datetime import datetime

from rest_framework import serializers

from django.utils import timezone
from django.db import transaction

from qlab.apps.company.models import (
    Company,
    LabDevice,
    MethodParameters,
    Proposal,
    ProposalDraft,
    ProposalMethodParameters,
    QualityMethod,
    Vehicle,
)
from qlab.apps.core.models import Notification
from qlab.apps.core.utils.offers_pdf_creater.invoice import InvoiceGenerator


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


class MethodParametersSerializers(serializers.ModelSerializer):
    method_names = serializers.SerializerMethodField()
    method_data = serializers.SerializerMethodField()

    class Meta:
        model = MethodParameters
        exclude = ('method',)

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
        exclude = ('user',)


class ProposalDraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProposalDraft
        fields = '__all__'


class ParametersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField()
    methods = serializers.ListField()


class ProposalSerializers(serializers.ModelSerializer):
    parameters = ParametersSerializer(many=True, required=False)

    class Meta:
        model = Proposal
        fields = '__all__'

    def create(self, validated_data):
        parameters_data = validated_data.pop('parameters', None)
        proposal = Proposal.objects.create(**validated_data)

        items = []
        for parameter_data in parameters_data:
            try:
                parameter = MethodParameters.objects.get(
                    id=parameter_data['id']
                )
                
            except MethodParameters.DoesNotExist:
                continue

            method_names = [
                  name for name in parameter_data['methods']
            ]

            measurement_name = ', '.join(method_names)
            items.append(
                {
                    'name': parameter.name,
                    'description': measurement_name,
                    'unit_price': parameter.price,
                    'quantity': parameter_data['count'],
                }
            )


        request = self.context.get('request')
        user = request.user

        invoice_generator = InvoiceGenerator(
            (user.full_name).upper(),
            items,
            8,
            proposal.draft.preface,
            proposal.draft.terms,
        )

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'{str(uuid4())[:8]}_{timestamp}.pdf'
        breakpoint()
        invoice_generator.generate_pdf(filename)
        proposal.file = f'/{filename}'
        proposal.save()
        return proposal
