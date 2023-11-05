GET_SCHEDULE_DATA_CLIENT = """
    SELECT
        sched.id,
        sched.schedule_date,
        ARRAY_AGG(services_list.serv_list) AS services
    FROM scheduler AS sched
    LEFT JOIN professional AS prof
        ON prof.id = sched.professional_id
    LEFT JOIN (
        SELECT
            serv.id,
            json_build_object(
                'id', serv.id,
                'name', serv.name,
                'time', serv.time,
                'value', serv.value
            ) AS serv_list
        FROM service AS serv
        GROUP BY serv.id
    ) AS services_list ON services_list.id = ANY(sched.services)
    WHERE 1=1
        AND sched.customer_phone = %(customer_phone)s
    GROUP BY sched.id, prof.id;
"""