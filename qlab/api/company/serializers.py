from rest_framework import serializers
from qlab.apps.accounts.models import User

from qlab.apps.company.models import Company, Vehicle

class VehicleSerializers(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields = '__all__'


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'
