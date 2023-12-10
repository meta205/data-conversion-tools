# -*- coding: utf-8 -*-

from data.base_data import BaseData
from data.util import file_utils
from . import excel_utils

import os
import xlrd
import xlwt


class ExcelData(BaseData):
    def __init__(self, filename):
        super().__init__(os.path.split(filename)[0])
        self.filename = filename
        self.workbook = xlrd.open_workbook(filename)

    def read(self):
        for sheet in self.workbook.sheets():
            columns = None

            for row_idx in range(sheet.nrows):
                if row_idx == 0:
                    columns = sheet.row_values(row_idx)
                    self.set_columns(sheet.name, columns)
                else:
                    old_values = sheet.row_values(row_idx)
                    new_values = []
                    for col_idx in range(len(old_values)):
                        cell_type = sheet.cell_type(row_idx, col_idx)
                        if cell_type == excel_utils.XL_CELL_DATE:
                            cell_type = excel_utils.XL_CELL_TIMESTAMP

                        if columns is not None:
                            column_info = self.get_column_info(sheet.name, columns[col_idx])
                            if column_info is not None:
                                cell_type = excel_utils.to_cell_type(column_info['type'])

                        new_values += [excel_utils.to_value(sheet, cell_type, old_values[col_idx])]

                    self.add_data(sheet.name, new_values)

    def write(self):
        workbook = xlwt.Workbook()

        style1 = xlwt.easyxf('font: bold True;'
                             'pattern: pattern solid, fore_colour gray25;'
                             'align: wrap on, vert centre, horiz left;'
                             'borders: top_color gray40, bottom_color gray40,'
                             'right_color gray40, left_color gray40,'
                             'left thin, right thin, top thin, bottom thin;')

        style2 = xlwt.easyxf('font: bold False;'
                             'pattern: pattern solid, fore_colour white;'
                             'align: wrap on, vert centre, horiz left;'
                             'borders: top_color gray40, bottom_color gray40,'
                             'right_color gray40, left_color gray40,'
                             'left thin, right thin, top thin, bottom thin;')

        for data_key in self.get_data_keys():
            sheet = workbook.add_sheet(data_key)
            sheet.show_grid = False
            sheet.set_panes_frozen(True)
            sheet.set_horz_split_pos(1)

            row_idx = 0
            for col_idx, value in enumerate(self.get_columns(data_key)):
                sheet.write(row_idx, col_idx, value, style1)
                sheet.row(row_idx).height_mismatch = True
                sheet.row(row_idx).height = 400

            data = self.get_data(data_key)
            for row_data in data:
                row_idx += 1
                for col_idx, value in enumerate(row_data):
                    sheet.write(row_idx, col_idx, value, style2)
                    sheet.row(row_idx).height_mismatch = True
                    sheet.row(row_idx).height = 400

        filename = file_utils.new_filename(self.filename)
        workbook.save(filename)
