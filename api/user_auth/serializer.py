from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers

from api.professional.models import Professionals

class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=250)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        Professionals.objects.create(
            user=user,
            phone=validated_data['phone'],
        )
        return user

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.first_name,
            'email': instance.email,
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid login credentials")
        return {'user': user}