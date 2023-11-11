class SchedulerStatus:
    SCHEDULED = 1
    DONE = 2
    CANCELED = 3
    

SCHEDULER_STATUS_CHOICES = (
    (SchedulerStatus.SCHEDULED, 'Agendado'),
    (SchedulerStatus.DONE, 'Finalizado'),
    (SchedulerStatus.CANCELED, 'Cancelado'),
)
