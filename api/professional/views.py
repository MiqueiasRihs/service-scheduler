from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied

from api.professional.models import Professional, WorkingPlan, Service
from api.professional.serializers import WorkingPlanSerializer, ServiceSerializer, CalculateServicesSerializer, \
    ScheduleSerializer
from api.utils.scheduler_class import SchedulerClass

from api.professional.utils import get_schedule_data_professional

class WorkingPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            professional = Professional.objects.get(user=user)
        except Professional.DoesNotExist:
            return NotFound(detail="Este profissional não esta cadastrado.")

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
            return NotFound(detail="Este profissional não esta cadastrado.")

        # Buscar os planos de trabalho associados ao profissional
        working_plans = WorkingPlan.objects.filter(professional=professional)

        # Serializar os planos de trabalho
        serializer = WorkingPlanSerializer(working_plans, many=True, context={'request': request})

        # Retornar os planos de trabalho serializados
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetIntervalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            professional = Professional.objects.get(user=request.user)
        except Professional.DoesNotExist:
            return NotFound(detail="Este profissional não esta cadastrado.")

        professional.interval = request.data.get('interval', 30)
        professional.save()

        return Response(status=status.HTTP_200_OK)


class ServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            professional = Professional.objects.get(user=request.user)
        except Professional.DoesNotExist:
            return NotFound(detail="Este profissional não esta cadastrado.")

        services = request.data

        # Criar serviços
        created_services = []
        for service_data in services:
            serializer = ServiceSerializer(data=service_data, context={'professional': professional})
            if serializer.is_valid():
                serializer.save()
                created_services.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_services, status=status.HTTP_201_CREATED)
    
    
    def get(self, request):
        try:
            professional = Professional.objects.get(user=request.user)
        except Professional.DoesNotExist:
            return NotFound(detail="Este profissional não esta cadastrado.")
            
        all_services = Service.objects.filter(professional=professional)
        serializer = ServiceSerializer(all_services, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UpdateServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, service_id):
        try:
            professional = Professional.objects.get(user=request.user)
        except Professional.DoesNotExist:
            return NotFound(detail="Este profissional não esta cadastrado.")
        
        try:
            service = Service.objects.get(id=service_id, professional=professional)
        except Service.DoesNotExist:
            return Response({"detail": f"O horário de trabalho não foi encontrado para este usuário. \
                                         Verifique se o ID do horário de trabalho está correto ou se pertence ao usuário autenticado."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "O serviço foi atualizado com sucesso"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentTimesAvailableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, professional_slug):
        try:
            professional = Professional.objects.get(slug=professional_slug)
        except Professional.DoesNotExist:
            return NotFound(detail="Este profissional não esta cadastrado")
            
        serializer = CalculateServicesSerializer(data=request.data)
        scheduler = SchedulerClass(professional)

        if serializer.is_valid():
            try:
                available_times = scheduler.get_available_times(request.data['date'])
                return Response(available_times, status=status.HTTP_200_OK)
            
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, schedule_date):
        try:
            professional = Professional.objects.get(user=request.user)
        except Professional.DoesNotExist:
            return NotFound(detail="Este profissional não esta cadastrado")

        schedules = get_schedule_data_professional(professional.id, schedule_date)
        serializer = ScheduleSerializer(schedules, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

