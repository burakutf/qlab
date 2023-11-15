from rest_framework import serializers


from qlab.apps.accounts.models import Role, User, UserDetail


class UserSerializers(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()

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
            'is_active',
            'date_joined',
            'phone',
            'birth_date',
            'gender',
            'vehicle',
            'company',
            'permissions',
            'role',
            'role_name',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        organization = request.user.organization

        if organization:
            validated_data['organization'] = organization
            return super().create(validated_data)

    def get_role_name(self, obj):
        if hasattr(obj, 'role') and obj.role is not None:
            return obj.role.name
        return ''


class UserDetailSerializers(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = UserDetail
        fields = '__all__'


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
