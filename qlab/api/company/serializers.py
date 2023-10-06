from rest_framework import serializers
from qlab.apps.accounts.models import User

from qlab.apps.company.models import Company, Vehicle


class VehicleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    vehicle_info = serializers.CharField(
        source='vehicle.plate', read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
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
            'vehicle_info',
            'company',
        )
