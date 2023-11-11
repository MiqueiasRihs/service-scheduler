from django.shortcuts import get_object_or_404

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
        data = request.data
        
        professional = get_object_or_404(Professional, slug=professional_slug)
        data['professional'] = professional.id

        scheduler = SchedulerClass(professional)
        try:
            data['end_time'] = scheduler.calculate_service_end_time(data)
            self.validate_services(data['services'], professional)
            self.check_availability(scheduler, data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({'error': str(e.detail)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'error': str(e.detail)}, status=status.HTTP_403_FORBIDDEN)

        serializer = BaseSchedulerSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        scheduling_data = serializer.validated_data

        Scheduler.objects.create(**scheduling_data)
        return Response({"message": "Agendamento criado com sucesso."}, status=status.HTTP_201_CREATED)


    def validate_services(self, services, professional):
        for service_id in services:
            if not Service.objects.filter(id=service_id, professional=professional).exists():
                raise NotFound(detail="Um dos serviços selecionados não pertence ao profissional em questão.")


    def check_availability(self, scheduler, scheduling_data):
        if not scheduler.is_available_schedule(scheduling_data):
            raise PermissionDenied(detail="Horário indisponível para agendamento.")

class GetSchedulerCustomerView(APIView):
    
    def get(self, request, phone):
        schedules = get_schedule_data_client(phone)
        serializer = ClientScheduleSerializer(schedules, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)