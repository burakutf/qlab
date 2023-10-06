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
    vehicle = serializers.SerializerMethodField()

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

    def get_vehicle(self, obj):
        if obj.vehicle:
            return obj.vehicle.plate
