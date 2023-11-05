from django.db import connection

from api.utils.utils import dictfetchall

from api.customer.sql_constants import GET_SCHEDULE_DATA_CLIENT

def get_schedule_data_client(customer_phone):
    with connection.cursor() as cursor:
        cursor.execute(GET_SCHEDULE_DATA_CLIENT, {
            'customer_phone': customer_phone
        })
        
        data = dictfetchall(cursor)

    return data