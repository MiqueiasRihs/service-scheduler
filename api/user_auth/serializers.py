from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

from api.professional.models import Professional

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['slug', 'phone', 'store', 'interval', 'instagram', 'profile_image_path']

class UserSerializer(serializers.ModelSerializer):
    professional = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'professional']

    def get_professional(self, user):
        # Presumindo que um usuário só tem um perfil Professional
        # Isso irá pegar o primeiro perfil Professional associado ao usuário
        professional = Professional.objects.filter(user=user).first()
        if professional:
            return ProfessionalSerializer(professional).data
        else:
            return None

class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=250)
    phone = serializers.CharField(max_length=15)
    instagram = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        # Check if the email already exists.
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Um usuário com este e-mail já existe.")
        return value

    def create(self, validated_data):
        # Create the user and professional instances
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        Professional.objects.create(
            user=user,
            phone=validated_data['phone'],
            # instagram=validated_data['instagram'] if validated_data["instagram"] else '',
        )
        return user

    def to_representation(self, instance):
        # Serialize user data
        return UserSerializer(instance).data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Authenticate the user
        user = authenticate(username=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Credenciais inválidas.")
        # If authentication is successful, return the user instance
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        # Serialize user data
        return UserSerializer(instance).data
