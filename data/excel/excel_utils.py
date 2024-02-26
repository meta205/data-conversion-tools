# -*- coding: utf-8 -*-

from data.util import data_utils

import datetime
import xlrd

# Original Excel Cell Type
XL_CELL_EMPTY = xlrd.XL_CELL_EMPTY
XL_CELL_TEXT = xlrd.XL_CELL_TEXT
XL_CELL_NUMBER = xlrd.XL_CELL_NUMBER
XL_CELL_DATE = xlrd.XL_CELL_DATE
XL_CELL_BOOLEAN = xlrd.XL_CELL_BOOLEAN
XL_CELL_ERROR = xlrd.XL_CELL_ERROR
XL_CELL_BLANK = xlrd.XL_CELL_BLANK

# Additional Excel Cell Type
XL_CELL_INTEGER = 7
XL_CELL_FLOAT = 8
XL_CELL_TIMESTAMP = 9
XL_CELL_TIME = 10


def to_cell_type(type):
    if type == 'string':
        return XL_CELL_TEXT
    elif type == 'number':
        return XL_CELL_NUMBER
    elif type == 'date':
        return XL_CELL_DATE
    elif type == 'time':
        return XL_CELL_TIME
    elif type == 'boolean':
        return XL_CELL_BOOLEAN
    elif type == 'integer':
        return XL_CELL_INTEGER
    elif type == 'float':
        return XL_CELL_FLOAT
    elif type == 'timestamp':
        return XL_CELL_TIMESTAMP

    return XL_CELL_TEXT


def to_value(sheet, cell_type, value):
    if cell_type == XL_CELL_DATE:
        return to_date(sheet, value)
    if cell_type == XL_CELL_TIME:
        return to_time(sheet, value)
    elif cell_type == XL_CELL_TIMESTAMP:
        return to_timestamp(sheet, value)
    elif cell_type == XL_CELL_TEXT:
        if isinstance(value, float):
            return str(int(value))
        if value is None:
            return ''
        return str(value)

    return value


def to_time(sheet, value):
    try:
        args = xlrd.xldate_as_tuple(value, sheet.book.datemode)
        return datetime.time(args[3], args[4], args[5])
    except:
        return value


def to_date(sheet, value):
    try:
        args = xlrd.xldate_as_tuple(value, sheet.book.datemode)
        return datetime.datetime(args[0], args[1], args[2])
    except:
        return value


def to_timestamp(sheet, value):
    try:
        args = xlrd.xldate_as_tuple(value, sheet.book.datemode)
        return datetime.datetime(args[0], args[1], args[2], args[3], args[4], args[5])
    except:
        return value
