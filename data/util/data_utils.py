# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone

import dateutil.parser


def is_integer(value):
    return str(value).isnumeric()


def is_number(value):
    try:
        float(str(value))
        return True
    except ValueError:
        return False


def is_date(value):
    try:
        if datetime.strptime(str(value), "%Y-%m-%d"):
            return True
        return False
    except ValueError:
        return False


def is_timestamp(value):
    try:
        if datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S"):
            return True
        return False
    except ValueError:
        return False


def get_data_type(column, value):
    column_name = column.upper()
    if column_name.endswith('ID') or column_name.endswith('CD') or column_name.endswith('NM'):
        return 'string'

    if column_name.endswith('TP') or column_name.endswith('UOM'):
        return 'string'

    if column_name.endswith('AT') or column_name.endswith('TS'):
        return 'timestamp'

    if column_name.endswith('FENCE') or column_name.endswith('PST') or column_name.endswith('PET'):
        return 'timestamp'

    if column_name.endswith('DT'):
        return 'date'

    if column_name.endswith('YN'):
        return 'boolean'

    if column_name.endswith('TM') or column_name.endswith('SEQ') or column_name.endswith('CNT'):
        return 'integer'

    if column_name.endswith('PRIORITY') or column_name.endswith('PERIOD'):
        return 'integer'

    if column_name.endswith('EFFICIENCY') or column_name.endswith('QTY'):
        return 'number'

    if column_name.endswith('MIN') or column_name.endswith('MAX') or column_name.endswith('MULTIPLR'):
        return 'number'

    str_value = str(value)
    if is_integer(str_value):
        return 'integer'
    elif is_number(str_value):
        return 'number'
    elif is_date(str_value):
        return 'date'
    elif is_timestamp(str_value):
        return 'timestamp'

    return 'string'


def to_string(column, value):
    data_type = get_data_type(column, value)
    if data_type == 'integer' or data_type == 'number':
        if len(str(value)) == 0:
            return '0' if data_type == 'integer' else '0.0'

        return str(value)

    if data_type == 'date' or data_type == 'timestamp':
        if is_number(str(value)):
            tz = timezone(timedelta(hours=9))
            new_value = (float(value) - 25569) * 86400.0
            return '\'%s\'' % str(datetime.fromtimestamp(new_value, timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))

        if len(str(value)) == 0:
            return 'NULL'

    return '\'%s\'' % value
