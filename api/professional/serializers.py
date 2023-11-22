from rest_framework import serializers

from api.professional.models import WorkingPlan, BreakTime, Service, Holiday
from api.professional.constants import HolidayType

from api.utils.utils import to_money

class BreakTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakTime
        fields = ['start_time', 'end_time']


class WorkingPlanSerializer(serializers.ModelSerializer):
    break_time = BreakTimeSerializer(many=True, required=False)

    class Meta:
        model = WorkingPlan
        fields = ['day_of_week', 'start_time', 'end_time', 'break_time']

    def create(self, validated_data):
        # Extrai os dados de break_time
        break_time_data = validated_data.pop('break_time', [])
        
        # Obtém ou cria um WorkingPlan com o mesmo day_of_week para o profissional
        professional = validated_data['professional']
        day_of_week = validated_data['day_of_week']

        working_plan, create = WorkingPlan.objects.update_or_create(
            professional=professional, 
            day_of_week=day_of_week, 
            defaults={
                'start_time': validated_data['start_time'],
                'end_time': validated_data['end_time']
            }
        )

        for break_data in break_time_data:
            BreakTime.objects.create(working_plan=working_plan, **break_data)

        return working_plan


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'time', 'value']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['time'] = instance.time.strftime("%H:%M") if instance.time else None
    #     return representation

    def create(self, validated_data):
        return Service.objects.create(professional=self.context['professional'], **validated_data)


class CalculateServicesSerializer(serializers.Serializer):
    services = serializers.ListField(child=serializers.UUIDField(), required=True)
    date = serializers.DateField(required=True)


class ScheduleSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    customer_name = serializers.CharField(max_length=255)
    customer_phone = serializers.CharField(max_length=20)
    schedule_date = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    services = ServiceSerializer(many=True)


class HolidaySerializer(serializers.ModelSerializer):
    holiday_type_description = serializers.SerializerMethodField()

    class Meta:
        model = Holiday
        fields = '__all__'
        extra_kwargs = {'professional': {'write_only': True, 'required': False}}

    def get_holiday_type_description(self, obj):
        return obj.get_holiday_type_display()

    def validate(self, data):
        # Extrair dia e mês da data do feriado
        holiday_date = data['date']
        day = holiday_date.day
        month = holiday_date.month

        # Verificar se existe um feriado com a mesma data (dia e mês) e professional
        query = Holiday.objects.filter(
            date__month=month, 
            date__day=day, 
            professional=self.context['professional']
        )

        if 'instance' in self.context:
            query = query.exclude(pk=self.context['instance'].pk)

        # Verificar se existem feriados duplicados
        if query.exists():
            raise serializers.ValidationError({
                'message': 'Já existe um feriado cadastrado para essa data para o profissional selecionado.'
            })
            
        if data['holiday_type'] == HolidayType.HALF_DAY:
            if not data.get('start_time') or not data.get('end_time'):
                raise serializers.ValidationError({
                    "message":"Para feriados de meio horário, a hora de inicio e hora de término são obrigatórios."
                })

        return data

    def create(self, validated_data):
        return Holiday.objects.create(**validated_data)