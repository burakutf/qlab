from rest_framework import serializers

from django.contrib.auth.models import Group, Permission

from qlab.apps.accounts.models import User


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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


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
