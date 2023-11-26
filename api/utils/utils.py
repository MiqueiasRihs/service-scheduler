import locale


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def to_money(amount):
    if not amount and amount != 0:
        return
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(float(amount), grouping=True)


def validate_phone(phone):
    phone = ''.join(filter(str.isdigit, phone))
    return phone