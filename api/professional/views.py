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

        created_plans = []

        # Validar e criar os planos de trabalho
        for plan_data in request.data:
            serializer = WorkingPlanSerializer(data=plan_data, context={'request': request})
            if serializer.is_valid():
                working_plan = serializer.save(professional=professional)
                created_plans.append(working_plan)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Serializar e retornar os objetos de working_plan criados
        response_serializer = WorkingPlanSerializer(created_plans, many=True, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    
    def get(self, request):
        user = request.user

        try:
            professional = Professional.objects.get(user=user)
        except Professional.DoesNotExist:
            return Response({"detail": "Usuário não tem um perfil de Profissional associado."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Buscar os planos de trabalho associados ao profissional
        working_plans = WorkingPlan.objects.filter(professional=professional)

        # Serializar os planos de trabalho
        serializer = WorkingPlanSerializer(working_plans, many=True, context={'request': request})

        # Retornar os planos de trabalho serializados
        return Response(serializer.data, status=status.HTTP_200_OK)