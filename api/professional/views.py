from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.utils.scheduler_class import SchedulerClass
from api.professional.models import Professional, WorkingPlan, Service, Holiday, BlockHour, Vacation, Absence
from api.professional.serializers import WorkingPlanSerializer, ServiceSerializer, CalculateServicesSerializer, \
    ScheduleSerializer, HolidaySerializer, BlockHourSerializer, VacationSerializer, UpdateProfessionalSerializer, \
    AbsenceSerializer

from api.professional.utils import get_schedule_data_professional, get_professional_data

from api.utils.utils import validate_phone

class ProfessionalUpdateData(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        professional = get_object_or_404(Professional, user=request.user)

        # Somente permitindo a atualização do Instagram, nome e telefone
        instagram = request.data.get('instagram')
        phone = request.data.get('phone')
        first_name = request.data.get('first_name')

        # Atualizando o profissional com as novas informações
        if instagram is not None:
            professional.instagram = instagram
        if phone is not None:
            professional.phone = validate_phone(phone)
        if first_name is not None:
            professional.user.first_name = first_name
            professional.slug = professional.generate_slug(first_name)
            professional.user.save()
        
        professional.save()
        
        # Serializando e retornando a resposta
        serializer = UpdateProfessionalSerializer(professional)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfessionalData(APIView):
    def get(self, request, professional_slug):
        professional = get_object_or_404(Professional, slug=professional_slug)
        data = get_professional_data(professional.id)
        return Response(data, status=status.HTTP_200_OK)


class WorkingPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professional = get_object_or_404(Professional, user=request.user)

        created_plans = []
        
        WorkingPlan.objects.filter(professional=professional).delete()
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
        professional = get_object_or_404(Professional, user=request.user)

        # Buscar os planos de trabalho associados ao profissional
        working_plans = WorkingPlan.objects.filter(professional=professional)

        # Serializar os planos de trabalho
        serializer = WorkingPlanSerializer(working_plans, many=True, context={'request': request})

        # Retornar os planos de trabalho serializados
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetIntervalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professional = get_object_or_404(Professional, user=request.user)
        professional.interval = request.data.get('interval', 30)
        professional.save()

        return Response(status=status.HTTP_200_OK)


class ServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        professional = get_object_or_404(Professional, user=request.user)
        service = request.data

        # Criar serviços
        serializer = ServiceSerializer(data=service, context={'professional': professional})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def get(self, request):
        professional = get_object_or_404(Professional, user=request.user)
        all_services = Service.objects.filter(professional=professional)
        serializer = ServiceSerializer(all_services, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UpdateServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, service_id):
        professional = get_object_or_404(Professional, user=request.user)
        
        try:
            service = Service.objects.get(id=service_id, professional=professional)
        except Service.DoesNotExist:
            return Response({"message": f"O horário de trabalho não foi encontrado para este usuário. \
                                         Verifique se o ID do horário de trabalho está correto ou se pertence ao usuário autenticado."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class DeleteServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, service_id):
        professional = get_object_or_404(Professional, user=request.user)
        
        try:
            service = Service.objects.get(id=service_id, professional=professional)
        except Service.DoesNotExist:
            return Response({"detail": f"O horário de trabalho não foi encontrado para este usuário. \
                                         Verifique se o ID do horário de trabalho está correto ou se pertence ao usuário autenticado."},
                            status=status.HTTP_404_NOT_FOUND)

        service.delete()
        return Response({"message": "O serviço foi deletado com sucesso"}, status=status.HTTP_200_OK)


class AppointmentTimesAvailableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, professional_slug):
        professional = get_object_or_404(Professional, slug=professional_slug)
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
        professional = get_object_or_404(Professional, user=request.user)
        schedules = get_schedule_data_professional(professional.id, schedule_date)
        serializer = ScheduleSerializer(schedules, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class HolidayCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professional = get_object_or_404(Professional, user=request.user)
        serializer = HolidaySerializer(data=request.data, context={'request': request, 'professional': professional})

        if serializer.is_valid():
            serializer.save(professional=professional)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class HolidayList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        professional = get_object_or_404(Professional, user=request.user)
        holidays = Holiday.objects.filter(professional=professional)
        serializer = HolidaySerializer(holidays, many=True)
        return Response(serializer.data)


class HolidayUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, holiday_id):
        holiday = get_object_or_404(Holiday, id=holiday_id)
        professional = get_object_or_404(Professional, user=request.user)

        # Verifica se o profissional que está fazendo a requisição é o mesmo associado ao feriado
        if holiday.professional != professional:
            return Response({'message': 'Você não tem permissão para atualizar este feriado.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = HolidaySerializer(holiday, data=request.data, context={'professional': professional, 'instance': holiday})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HolidayDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, holiday_id):
        holiday = get_object_or_404(Holiday, id=holiday_id)
        professional = get_object_or_404(Professional, user=request.user)

        # Verifica se o profissional que está fazendo a requisição é o mesmo associado ao feriado
        if holiday.professional != professional:
            return Response({'message': 'Você não tem permissão para deletar este feriado.'}, status=status.HTTP_403_FORBIDDEN)

        holiday.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    
class BlockHourList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professional = get_object_or_404(Professional, user=request.user)
        date = request.data.get('date')

        # Verifica se já existe um BlockHour com a mesma data para o profissional
        block_hour_instance = BlockHour.objects.filter(date=date, professional=professional).first()

        if block_hour_instance:
            # Se já existe, atualiza o registro existente
            serializer = BlockHourSerializer(block_hour_instance, data=request.data, context={'professional': professional})
        else:
            # Se não existe, cria um novo
            serializer = BlockHourSerializer(data=request.data, context={'professional': professional})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if not block_hour_instance else status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        professional = get_object_or_404(Professional, user=request.user)
        
        date = request.query_params.get('date')
        block_times = BlockHour.objects.filter(professional=professional, date=date).first()
        serializer = BlockHourSerializer(block_times)

        if block_times:
            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    

class VacationList(APIView):
    permission_classes = [IsAuthenticated]
    
    """
    List all vacations or create a new vacation.
    """
    def get(self, request, format=None):
        professional = get_object_or_404(Professional, user=request.user)
        
        vacations = Vacation.objects.filter(professional=professional)
        serializer = VacationSerializer(vacations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        professional = get_object_or_404(Professional, user=request.user)

        serializer = VacationSerializer(data=request.data, context={'professional': professional})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VacationDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, vacations_id, format=None):
        professional = get_object_or_404(Professional, user=request.user)
        vacation = get_object_or_404(Vacation, pk=vacations_id, professional=professional)
        vacation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AbsenceCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professional = get_object_or_404(Professional, user=request.user)
        serializer = AbsenceSerializer(data=request.data, context={'request': request, 'professional': professional})

        if serializer.is_valid():
            serializer.save(professional=professional)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AbsenceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        professional = get_object_or_404(Professional, user=request.user)
        abscences = Absence.objects.filter(professional=professional)
        serializer = AbsenceSerializer(abscences, many=True)
        return Response(serializer.data)


class AbsenceUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, absence_id):
        absence = get_object_or_404(Absence, id=absence_id)
        professional = get_object_or_404(Professional, user=request.user)

        # Verifica se o profissional que está fazendo a requisição é o mesmo associado ao feriado
        if absence.professional != professional:
            return Response({'message': 'Você não tem permissão para atualizar esta ausencia.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AbsenceSerializer(absence, data=request.data, context={'professional': professional, 'instance': absence})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbsenceDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, absence_id):
        absence = get_object_or_404(Absence, id=absence_id)
        professional = get_object_or_404(Professional, user=request.user)

        # Verifica se o profissional que está fazendo a requisição é o mesmo associado ao feriado
        if absence.professional != professional:
            return Response({'message': 'Você não tem permissão para deletar este feriado.'}, status=status.HTTP_403_FORBIDDEN)

        absence.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)