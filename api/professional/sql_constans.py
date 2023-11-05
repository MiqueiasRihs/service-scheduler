GET_SCHEDULE_DATA_PROFESSIONAL = """
    SELECT
        sched.id,
        sched.customer_name,
        sched.customer_phone,
        sched.schedule_date,
        sched.end_time,
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
        AND sched.professional_id = %(professional_id)s
        AND DATE(sched.schedule_date) = %(schedule_date)s
    GROUP BY sched.id, prof.id;
"""