from rest_framework import serializers


from qlab.apps.accounts.models import Role, User


class UserSerializers(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name')

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
            'permissions',
            'role',
            'role_name',
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
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
