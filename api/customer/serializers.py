from rest_framework import serializers

from api.professional.serializers import ServiceSerializer


class BaseSchedulerSerializer(serializers.Serializer):
    schedule_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    services = serializers.ListField(
        child=serializers.IntegerField(min_value=1), 
        allow_empty=False
    )
    customer_name = serializers.CharField(max_length=100)
    customer_phone = serializers.CharField(max_length=20)


class ClientScheduleSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    schedule_date = serializers.DateTimeField()
    services = ServiceSerializer(many=True)
