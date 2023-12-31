from datetime import datetime, timedelta, time

from api.professional.models import Service, WorkingPlan, BreakTime, Holiday, BlockHour, Vacation, Absence
from api.professional.constants import HolidayType

from api.customer.models import Scheduler

import math

class SchedulerClass:
    MAX_SERVICES_LIMIT = 100


    def __init__(self, professional):
        self.professional = professional


    def calculate_total_time(self, services_ids):
        services = Service.objects.filter(id__in=services_ids)
        if services.count() != len(services_ids):
            raise ValueError(f"Alguns dos serviços passados não existem")

        total_time = timedelta().seconds
        for service in services:
            total_time += timedelta(hours=service.time.hour, minutes=service.time.minute).seconds

        total_time = time(total_time // 3600, (total_time % 3600) // 60)
        return total_time


    def calculate_service_end_time(self, scheduling):
        total_time = self.calculate_total_time(scheduling['services'])
        date_time_obj = datetime.strptime(scheduling['schedule_date'], '%Y-%m-%d %H:%M:%S.%f')
        total_time_delta = timedelta(hours=total_time.hour, minutes=total_time.minute)
        result_datetime = date_time_obj + total_time_delta
        return result_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')


    def get_available_times(self, date):
        unavailable_hours = []
        current_datetime = datetime.now()
        data_datetime = datetime.strptime(date, "%Y-%m-%d")
        
        print("WEEKDAY >>> ", data_datetime.weekday())
        
        if self._check_vacations(data_datetime, self.professional):
            return []

        holiday = Holiday.objects.filter(date=data_datetime).first()
        if holiday and holiday.holiday_type == HolidayType.FULL_DAY:
            return []
        elif holiday and holiday.holiday_type == HolidayType.HALF_DAY:
            working_plan = holiday
        else:
            try:
                working_plan = WorkingPlan.objects.get(day_of_week=data_datetime.weekday(), professional=self.professional)
            except WorkingPlan.DoesNotExist:
                return []

            break_times = BreakTime.objects.filter(working_plan=working_plan)
            for break_time in break_times:
                unavailable_hours.append(
                    (datetime.strptime(break_time.start_time, '%H:%M'), datetime.strptime(break_time.end_time, '%H:%M'))
                )

        schedules = Scheduler.objects.filter(schedule_date__date=date, professional=self.professional)
        for schedule in schedules:
            start_time = schedule.schedule_date.strftime('%H:%M')
            end_time = schedule.end_time.strftime('%H:%M')
            unavailable_hours.append(
                (datetime.strptime(start_time, '%H:%M'), datetime.strptime(end_time, '%H:%M'))
            )

        start_time = datetime.strptime(working_plan.start_time, '%H:%M')
        end_time = datetime.strptime(working_plan.end_time, '%H:%M')
        
        available_times = []
        interval = timedelta(minutes=self.professional.interval)
        current_time = datetime.strptime(working_plan.start_time, '%H:%M')

        while current_time <= datetime.strptime(working_plan.end_time, '%H:%M'):
            is_available = all(
                current_time < break_start or current_time >= break_end
                for break_start, break_end in unavailable_hours
            )
            # Convertendo current_time para datetime completo para comparação
            full_current_time = data_datetime.replace(hour=current_time.hour, minute=current_time.minute)

            if is_available and full_current_time >= current_datetime:
                available_times.append(current_time.strftime('%H:%M'))
            current_time += interval

        # Remoção de horários bloqueados
        available_times = self._remove_block_hours(available_times[:-1], data_datetime)
        available_times = self._check_absences(data_datetime, available_times)

        return available_times
    
    
    def _check_absences(self, date, available_times):
        absences = Absence.objects.filter(professional=self.professional, date=date)
        
        # Converter available_times para objetos datetime.time
        available_times_as_time_objects = [
            datetime.strptime(time_str, "%H:%M").time() for time_str in available_times
        ]
        
        # Verificar ausências e remover horários conflitantes
        for absence in absences:
            if absence.absence_type == HolidayType.FULL_DAY:
                # Se for uma ausência de dia inteiro, limpar todos os horários disponíveis
                return []
            elif absence.absence_type == HolidayType.HALF_DAY:
                # Converter horários de início e término para objetos datetime.time
                start_time = datetime.strptime(absence.start_time, "%H:%M").time()
                end_time = datetime.strptime(absence.end_time, "%H:%M").time()
                
                # Filtrar os horários disponíveis removendo aqueles que estão dentro do intervalo de ausência
                available_times_as_time_objects = [
                    time_obj for time_obj in available_times_as_time_objects
                    if not (start_time <= time_obj < end_time)
                ]
        
        # Converter de volta para strings no formato HH:MM após o processamento
        available_times = [time_obj.strftime("%H:%M") for time_obj in available_times_as_time_objects]
        
        return available_times

    def _remove_block_hours(self, available_times, date):
        block_hour = BlockHour.objects.filter(date=date).first()

        if block_hour:
            # Converte os horários bloqueados para o formato de hora necessário
            blocked_times_formatted = [hour.strftime('%H:%M') for hour in block_hour.hours]

            # Remove os horários bloqueados da lista de horários disponíveis
            available_times = [time for time in available_times if time not in blocked_times_formatted]

        return available_times
    
    
    def _check_vacations(self, date, professional):
        vacations = Vacation.objects.filter(professional=professional)
        for vacation in vacations:
            date_to_compare = date.date() if isinstance(date, datetime) else date

            if vacation.start_date <= date_to_compare <= vacation.end_date:
                return True

        return False


    def generate_time_slots(self, scheduler):
        interval = timedelta(minutes=self.professional.interval)
        start_time = datetime.strptime(scheduler['schedule_date'], '%Y-%m-%d %H:%M:%S.%f')
        end_time = datetime.strptime(scheduler['end_time'], '%Y-%m-%d %H:%M:%S.%f')

        # Lista para armazenar os horários gerados
        time_slots = []

        # Loop para gerar os horários
        current_time = start_time
        while current_time < end_time:
            # Adiciona o horário atual à lista no formato HH:MM
            time_slots.append(current_time.strftime('%H:%M'))
            # Incrementa o horário atual com o intervalo
            current_time += interval

        return time_slots


    def is_available_schedule(self, scheduler):
        datetime_obj = datetime.strptime(scheduler["schedule_date"], "%Y-%m-%d %H:%M:%S.%f")
        date_obj = datetime_obj.date().strftime("%Y-%m-%d")

        available_times = self.get_available_times(date_obj)
        necessary_time_slots = self.generate_time_slots(scheduler)
        
        return all(item in available_times for item in necessary_time_slots)
