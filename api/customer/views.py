from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, JsonResponse

from api.professional.models import Professional, Service

from api.utils.scheduler_class import SchedulerClass

from api.customer.models import Scheduler
from api.customer.utils import get_schedule_data_client
from api.customer.serializers import BaseSchedulerSerializer, ClientScheduleSerializer

class SchedulerCreateView(APIView):
    def post(self, request, professional_slug):
        serializer = BaseSchedulerSerializer(data=request.data)
        if serializer.is_valid():
            scheduling_data = serializer.validated_data

        try:
            professional = Professional.objects.get(slug=professional_slug)
        except Professional.DoesNotExist:
            raise NotFound(detail="Este profissional não está cadastrado.")

        scheduler = SchedulerClass(professional)
        scheduling_data = request.data
        scheduling_data['professional_id'] = professional.id

        try:
            scheduling_data['end_time'] = scheduler.calculate_service_end_time(scheduling_data)
        except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        for service_id in scheduling_data.get('services', []):
            if not Service.objects.filter(id=service_id, professional=professional).exists():
                raise NotFound(detail="Um dos serviços selecionados não pertence ao profissional em questão.")

        if not scheduler.is_available_schedule(scheduling_data):
            raise PermissionDenied(detail="Horário indisponível para agendamento.")
        
        Scheduler.objects.create(**scheduling_data)

        return JsonResponse({"message": "Agendamento criado com sucesso."}, status=status.HTTP_201_CREATED)


class GetSchedulerCustomerView(APIView):
    
    def get(self, request, phone):
        schedules = get_schedule_data_client(phone)
        serializer = ClientScheduleSerializer(schedules, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)