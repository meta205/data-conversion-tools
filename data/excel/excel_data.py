# -*- coding: utf-8 -*-

from data.base_data import BaseData
from data.util import file_utils
from . import excel_utils

import os
import xlrd
import xlsxwriter


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
        filename = file_utils.new_filename(self.filename)
        workbook = xlsxwriter.Workbook(filename)

        cell_format1 = workbook.add_format({
            'bold': True,
            'font_color': '#FFFFFF',
            'bg_color': '#404040',
            'top': 1,
            'bottom': 1,
            'left': 1,
            'right': 1,
            'top_color': '#666666',
            'bottom_color': '#666666',
            'left_color': '#666666',
            'right_color': '#666666'
        })

        cell_format2 = workbook.add_format({
            'bold': False,
            'font_color': '#000000',
            'bg_color': '#FFFFFF',
            'top': 1,
            'bottom': 1,
            'left': 1,
            'right': 1,
            'top_color': '#666666',
            'bottom_color': '#666666',
            'left_color': '#666666',
            'right_color': '#666666'
        })

        for data_key in self.get_data_keys():
            worksheet = workbook.add_worksheet(data_key)
            worksheet.freeze_panes(1, 0)
            worksheet.hide_gridlines(2)

            row_idx = 0
            for col_idx, value in enumerate(self.get_columns(data_key)):
                worksheet.write(row_idx, col_idx, value, cell_format1)

            data = self.get_data(data_key)
            for row_data in data:
                row_idx += 1
                for col_idx, value in enumerate(row_data):
                    worksheet.write(row_idx, col_idx, value, cell_format2)

            worksheet.autofit()

        workbook.close()
