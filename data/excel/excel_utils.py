# -*- coding: utf-8 -*-

import datetime
import xlrd


def convert_values(sheet, row_idx, values):
    new_value = []
    for col_idx in range(len(values)):
        cell_type = sheet.cell_type(row_idx, col_idx)
        if cell_type == 3:
            new_value += [convert_to_datetime(sheet, values[col_idx])]
        else:
            new_value += [values[col_idx]]

    return new_value


def convert_to_datetime(sheet, value):
    try:
        args = xlrd.xldate_as_tuple(value, sheet.book.datemode)
        return datetime.datetime(args[0], args[1], args[2], args[3], args[4], args[5])
    except:
        return value
