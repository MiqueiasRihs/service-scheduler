from datetime import datetime, timedelta, time

from api.professional.models import Service, WorkingPlan, BreakTime

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

    def get_available_times(self, date, total_time_services):
        unavailable_hours = []
        data_datetime = datetime.strptime(date, "%Y-%m-%d")
        
        working_plan = WorkingPlan.objects.get(day_of_week=data_datetime.weekday(), professional=self.professional)
        break_times = BreakTime.objects.filter(working_plan=working_plan)
        schedules = Scheduler.objects.filter(schedule_date=date)
        
        for schedule in schedules:
            start_time = schedule.schedule_date.strftime('%H:%M')
            end_time = schedule.end_time.strftime('%H:%M')
            unavailable_hours.append(
                (datetime.strptime(start_time, '%H:%M'), datetime.strptime(end_time, '%H:%M'))
            )

        for break_time in break_times:
            unavailable_hours.append(
                (datetime.strptime(break_time.start_time, '%H:%M'), datetime.strptime(break_time.end_time, '%H:%M'))
            )

        start_time = datetime.strptime(working_plan.start_time, '%H:%M')
        end_time = datetime.strptime(working_plan.end_time, '%H:%M')
        
        available_times = []
        interval = timedelta(minutes=self.professional.interval)
        current_time = start_time

        while current_time <= end_time:
            is_available = all(
                current_time < break_start or current_time >= break_end
                for break_start, break_end in unavailable_hours
            )

            if is_available:
                available_times.append(current_time.strftime('%H:%M'))
            current_time += interval
        
        return self.filter_sequential_times(available_times, total_time_services, date, interval)

    def filter_sequential_times(self, available_times, service_duration, date, interval):
        schedule_date = datetime.strptime(date, '%Y-%m-%d')
        service_duration = timedelta(hours=service_duration.hour, minutes=service_duration.minute)
        
        converted_times = [(time_str, schedule_date.replace(hour=int(time_str.split(':')[0]), minute=int(time_str.split(':')[1])))
                           for time_str in available_times]
        sequential_times = []
        for i in range(len(converted_times) - 1):
            current = timedelta(hours=converted_times[i][1].hour, minutes=converted_times[i][1].minute).seconds
            next_time = timedelta(hours=converted_times[i + 1][1].hour, minutes=converted_times[i + 1][1].minute).seconds
            
            if (next_time - current) == interval.seconds or service_duration.seconds <= interval.seconds:
                sequential_times.append((available_times[i], converted_times[i][1]))

        num_required = math.ceil(service_duration.seconds / interval.seconds)
        diff = len(sequential_times) % num_required
        if diff > 0:
            sequential_times = sequential_times[:-diff]

        return [time[0] for time in sequential_times]

    def is_available_schedule(self, scheduling):
        datetime_obj = datetime.strptime(scheduling["schedule_date"], "%Y-%m-%d %H:%M:%S.%f")
        endtime_obj = datetime.strptime(scheduling["end_time"], "%Y-%m-%d %H:%M:%S.%f")
        date_obj = datetime_obj.date().strftime("%Y-%m-%d")
        total_time_services = self.calculate_total_time(scheduling["services"])
        available_times = self.get_available_times(date_obj, total_time_services)
        start_time = datetime_obj

        while start_time.time() < endtime_obj.time():
            if start_time.strftime('%H:%M') not in available_times:
                return False
            start_time += timedelta(minutes=self.professional.interval)

        return True

    def calculate_total_cost(self, services):
        total_cost = 0
        for service in services:
            total_cost += service.value
        return total_cost
