# -*- coding: utf-8 -*-

import argparse
import csv
import datetime
import os
import pandas as pd
import xlrd


def convert_value(workbook, name, value):
    if name.endswith('_AT') or name.endswith('_TS'):
        try:
            args = xlrd.xldate_as_tuple(value, workbook.datemode)
            return datetime.datetime(args[0], args[1], args[2], args[3], args[4], args[5])
        except:
            return None
    elif name.endswith('_DT') or name.endswith('_DT_FENCE') or name == 'PST' or name == 'PET':
        try:
            args = xlrd.xldate_as_tuple(value, workbook.datemode)
            return datetime.date(args[0], args[1], args[2])
        except:
            return None

    return value


def to_cvs(filename):
    workbook = xlrd.open_workbook(filename)
    sheet_names = workbook.sheet_names()

    if len(sheet_names) == 0:
        return

    dirname = os.path.splitext(os.path.basename(filename))[0]
    os.mkdir(os.path.join('.', dirname))

    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name)
        if sheet.nrows < 2:
            continue

        writer = csv.writer(open(os.path.join('.', dirname, '%s.csv' % sheet_name), 'w', newline=''))

        names = []
        for row in range(sheet.nrows):
            values = sheet.row_values(row)
            if row == 0:
                names = values[:]
            else:
                values = [convert_value(workbook, names[i], v) for i, v in enumerate(values)]

            writer.writerow(values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='target file path')

    args = parser.parse_args()
    to_cvs(args.path)


if __name__ == '__main__':
    main()
