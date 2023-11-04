from rest_framework import serializers

class BaseSchedulerSerializer(serializers.Serializer):
    schedule_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f")
    services = serializers.ListField(
        child=serializers.IntegerField(min_value=1), 
        allow_empty=False
    )
    customer_name = serializers.CharField(max_length=100)
    customer_phone = serializers.CharField(max_length=20)
