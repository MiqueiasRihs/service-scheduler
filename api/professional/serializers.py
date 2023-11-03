from rest_framework import serializers

from api.professional.models import WorkingPlan, BreakTime, Service, Professional

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
        
        # Verifica se já existe um WorkingPlan com o mesmo day_of_week para o profissional
        professional = validated_data['professional']
        day_of_week = validated_data['day_of_week']

        working_plan, created = WorkingPlan.objects.update_or_create(
            professional=professional, 
            day_of_week=day_of_week, 
            defaults={
                'start_time': validated_data['start_time'],
                'end_time': validated_data['end_time']
            }
        )

        # Atualiza ou cria os BreakTimes associados
        BreakTime.objects.filter(working_plan=working_plan).delete()
        for break_data in break_time_data:
            BreakTime.objects.update_or_create(working_plan=working_plan, **break_data)

        return working_plan


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'time', 'value']

    def create(self, validated_data):
        return Service.objects.create(professional=self.context['professional'], **validated_data)