from django.db import connection

from api.utils.utils import dictfetchall

from api.professional.sql_constans import GET_SCHEDULE_DATA_PROFESSIONAL, GET_PROFESSIONAL_DATA

def get_schedule_data_professional(professional_id, schedule_date):
    with connection.cursor() as cursor:
        cursor.execute(GET_SCHEDULE_DATA_PROFESSIONAL, {
            'professional_id': professional_id,
            'schedule_date': schedule_date
        })
        data = dictfetchall(cursor)

    return data

def get_professional_data(professional_id):
    with connection.cursor() as cursor:
        cursor.execute(GET_PROFESSIONAL_DATA, {
            'professional_id': professional_id
        })
        data = dictfetchall(cursor)

    return data