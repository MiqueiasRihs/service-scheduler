from datetime import datetime, timedelta, time

from api.professional.models import Service, WorkingPlan, BreakTime, Scheduling

import math


MAX_SERVICES_LIMIT = 100


def calculate_total_time(services):
    services = Service.objects.filter(id__in=services)
    total_time = timedelta(hours=0, minutes=0).seconds
    
    for service in services:
        total_time += timedelta(hours=service.time.hour, minutes=service.time.minute).seconds

    total_time = time(total_time // 3600, (total_time % 3600) // 60)

    return total_time


def calculate_service_end_time(scheduling):
    total_time = calculate_total_time(scheduling.services)
    
    # Convert the string to a datetime object
    date_time_obj = datetime.strptime(scheduling.schedule_date, '%Y-%m-%d %H:%M:%S.%f')
    
    # Convert the total time to a timedelta object
    total_time_delta = timedelta(hours=total_time.hour, minutes=total_time.minute)
    
    # Calculate the result as a datetime object
    result_datetime = date_time_obj + total_time_delta
    
    # Format the result as a string
    result_string = result_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    return result_string


def get_available_times(date, professional, total_time_services):
    """
    Retrieves the available times for scheduling based on the specified date, professional ID, and total service time.

    Args:
        db: Database object for querying the data.
        date (str): Date of the scheduling.
        professional.id (int): ID of the professional.
        total_time_services (timedelta): Total time required for the services.

    Returns:
        list: List of available times for scheduling.
    """
    unavailable_hours = []
    data_datetime = datetime.strptime(date, "%Y-%m-%d")
    
    working_plan = WorkingPlan.objects.get(day_of_week=data_datetime.weekday(), professional=professional)
    break_times = BreakTime.objects.filter(working_plan=working_plan)
    schedules = Scheduling.objects.filter(schedule_date=date)
    
    # Populate the list of unavailable hours with existing schedules and break times
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
    
    # Convert start and end times to datetime objects
    start_time = datetime.strptime(working_plan.start_time, '%H:%M')
    end_time = datetime.strptime(working_plan.end_time, '%H:%M')

    available_times = []

    # Create a 30-minute interval
    interval = timedelta(minutes=professional.interval)

    # Initialize the current time with the start time
    current_time = start_time

    # While the current time is less than the end time
    while current_time <= end_time:
        # Check if the current time is not within any break interval
        is_available = all(
            current_time < break_start or current_time >= break_end
            for break_start, break_end in unavailable_hours
        )

        if is_available:
            # Add the current time to the list of available times
            available_times.append(current_time.strftime('%H:%M'))

        # Advance the current time by 30 minutes
        current_time += interval

    available_times = filter_sequential_times(available_times, total_time_services, date, interval)
    return available_times


def filter_sequential_times(available_times, service_duration, date, interval):
    """
    Filters the available times to find sequential times that can accommodate the service within the given time interval.

    Args:
        available_times (list): List of available times.
        service_duration (timedelta): Service duration.
        date (str): Date of the service.
        interval (int): Time interval between sequential times.

    Returns:
        list: List of sequential available times that can accommodate the service.
    """
    # Convert the date string to a datetime object
    schedule_date = datetime.strptime(date, '%Y-%m-%d')

    # Convert the service duration to the appropriate format
    service_duration = timedelta(hours=service_duration.hour, minutes=service_duration.minute)
    
    # Convert the time strings to datetime objects
    converted_times = []
    for time_str in available_times:
        hour, minute = map(int, time_str.split(':'))
        time_obj = time(hour, minute)
        converted_times.append((time_str, schedule_date.replace(hour=time_obj.hour, minute=time_obj.minute)))

    # Check if the times are sequential based on the given interval
    sequential_times = []
    for i in range(len(converted_times)):
        if converted_times[-1][1] == converted_times[i][1]:
            break

        current = timedelta(hours=converted_times[i][1].hour, minutes=converted_times[i][1].minute).seconds
        next_time = timedelta(hours=converted_times[i + 1][1].hour, minutes=converted_times[i + 1][1].minute).seconds

        if (service_duration.seconds <= interval.seconds) or (next_time - current) == interval.seconds:
            sequential_times.append((available_times[i], converted_times[i][1]))
    
    # Calculate the number of required intervals
    num_required = math.ceil(service_duration.seconds / interval.seconds)

    # Adjust the sequential times to match the required intervals
    diff = len(sequential_times) % num_required
    if diff > 0:
        sequential_times = sequential_times[:-diff]

    # Extract the times from the sequential times list
    final_list = [time[0] for time in sequential_times]

    return final_list


def is_available_schedule(professional, scheduling):
    # Convert the scheduling date to a datetime object
    datetime_obj = datetime.strptime(scheduling.schedule_date, "%Y-%m-%d %H:%M:%S.%f")
    endtime_obj = datetime.strptime(scheduling.end_time, "%Y-%m-%d %H:%M:%S.%f")
    # Extract only the date
    date_obj = datetime_obj.date().strftime("%Y-%m-%d")

    # Get the available times for the specified date and professional
    total_time_services = calculate_total_time(scheduling.services)
    available_times = get_available_times(date_obj, professional, total_time_services)

    # Convert the scheduling start time to a datetime object
    start_time = datetime.strptime(scheduling.schedule_date, '%Y-%m-%d %H:%M:%S.%f')

    time_slots = []
    # Generate time slots in 30-minute intervals
    while start_time.time() < endtime_obj.time():
        time_slots.append(start_time.strftime('%H:%M'))

        # Check if the generated time slot is in the list of available times
        if not start_time.strftime('%H:%M') in available_times:
            return False  # Scheduling is not available
        
        start_time += timedelta(minutes=professional.interval)

    return True  # Scheduling is available


def calculate_total_cost(services):
    total_cost = 0

    for service in services:
        total_cost += service.value

    return total_cost
        