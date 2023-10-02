from rest_framework import serializers

class VehicleSerializers(serializers.Serializer):
    class Meta:
        fields = '__all__'


class CompanySerializers(serializers.Serializer):
    class Meta:
        fields = '__all__'


class UserSerializers(serializers.Serializer):
    class Meta:
        fields = '__all__'
