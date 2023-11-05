from django.db import connection

from api.utils.utils import dictfetchall

from api.professional.sql_constans import GET_SCHEDULE_DATA_PROFESSIONAL

def get_schedule_data_professional(professional_id, schedule_date):
    with connection.cursor() as cursor:
        cursor.execute(GET_SCHEDULE_DATA_PROFESSIONAL, {
            'professional_id': professional_id,
            'schedule_date': schedule_date
        })
        data = dictfetchall(cursor)

    return data