# serializers.py
from django.core.serializers import serialize
from rest_framework import serializers
from .models import MyUser, Module, CustomPermission, Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         user = self.user
#         refresh = self.get_token(user)
#         # Serialize the role object to a JSON-serializable format
#         role_data = serialize('json', [user.role])
#         # role_data = role_data[1:-1]  # Remove brackets from the serialized data
#
#         data['user'] = {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'role':role_data
#             # Include any other user information you want
#         }
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         return data
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = self.get_token(user)
        # Get role and its privileges
        role = user.role
        module=user.module
        module_name = module.name if module else None
        role_name = role.name if role else None
        role_privileges = []
        module_privileges = []
        if role:
            role_privileges = list(role.permissions.values_list('codename', flat=True))
        if module:
            module_privileges = list(module.custompermission_set.values_list('permission__codename', flat=True))

        # Customize the response data here
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,

        }
        data['module']= module_name
        data['role'] = role_name
        data['module_privileges'] = module_privileges
        data['role_privileges'] = role_privileges
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'username', 'password', 'role','module')  # Include fields you want to expose
        extra_kwargs = {'password': {'write_only': True}}  # Make the password write-only

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class CustomPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
