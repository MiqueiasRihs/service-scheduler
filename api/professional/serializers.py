from rest_framework import serializers

from api.professional.models import WorkingPlan, BreakTime

class BreakTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakTime
        fields = ['start_time', 'end_time']

class WorkingPlanSerializer(serializers.ModelSerializer):
    break_time = BreakTimeSerializer(many=True)

    class Meta:
        model = WorkingPlan
        fields = ['day_of_week', 'start_time', 'end_time', 'break_time']

    def create(self, validated_data):
        # Extrai os dados de break_time
        break_time_data = validated_data.pop('break_time')
        
        # Cria a instância de WorkingPlan
        working_plan = WorkingPlan.objects.create(**validated_data)
        
        # Cria as instâncias de BreakTime associadas ao WorkingPlan
        for break_data in break_time_data:
            BreakTime.objects.create(working_plan=working_plan, **break_data)
        
        return working_plan
