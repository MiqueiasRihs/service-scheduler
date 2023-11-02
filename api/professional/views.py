from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.professional.models import Professional, WorkingPlan, BreakTime
from api.professional.serializers import WorkingPlanSerializer


class WorkingPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            professional = Professional.objects.get(user=user)
        except Professional.DoesNotExist:
            return Response({"detail": "Usuário não tem um perfil de Profissional associado."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validar e criar os planos de trabalho
        for plan_data in request.data:
            serializer = WorkingPlanSerializer(data=plan_data)
            if serializer.is_valid():
                existing_plan = WorkingPlan.objects.filter(day_of_week=plan_data['day_of_week'],
                                                           professional=professional)
                if existing_plan.exists():
                    return Response({"detail": f"O dia {plan_data['day_of_week']} já existe, tente atualizá-lo."},
                                    status=status.HTTP_409_CONFLICT)

                working_plan = serializer.save(professional=professional)

                # Criar os horários de intervalo associados, se houver
                for break_data in plan_data.get('break_time', []):
                    BreakTime.objects.create(
                        working_plan=working_plan, **break_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Plano de trabalho criado com sucesso."}, status=status.HTTP_201_CREATED)
