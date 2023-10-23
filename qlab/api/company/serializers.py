from rest_framework import serializers
from qlab.apps.accounts.models import  User
from django.utils import timezone

from qlab.apps.company.models import Company, LabDevice, MethodParameters, QualityMethod, Vehicle
from qlab.apps.core.models import Notification


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

class MinimalQualityMethodSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = QualityMethod
        fields = ('id','measurement_number',)



class MethodParametersSerializers(serializers.ModelSerializer):
    method_names = serializers.SerializerMethodField()

    class Meta:
        model = MethodParameters
        fields = '__all__'

    def get_method_names(self, obj):
        method_names = [method.measurement_number for method in obj.method.all()]
        return method_names


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


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'password',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'phone',
            'is_superuser',
            'birth_date',
            'gender',
            'vehicle',
            'company',
        )


class MinimalUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'is_staff',
            'is_active',
            'is_superuser',
        )
