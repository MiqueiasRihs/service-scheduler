from rest_framework import serializers

from api.professional.serializers import ServiceSerializer

from api.customer.models import Scheduler

import phonenumbers


class BaseSchedulerSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(max_length=150)
    customer_phone = serializers.CharField(max_length=15)
    schedule_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    services = serializers.ListField(child=serializers.UUIDField(), allow_empty=False)
    
    class Meta:
        model = Scheduler
        fields = '__all__'
    
    def validate_customer_phone(self, value):
        phone_number = phonenumbers.parse(value, "BR")
        if not phonenumbers.is_valid_number(phone_number):
            raise serializers.ValidationError({"message": "Número de telefone inválido"})

        return ''.join(char for char in value if char.isdigit())
        

class ClientScheduleSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    schedule_date = serializers.DateTimeField()
    services = ServiceSerializer(many=True)
