# -*- coding: utf-8 -*-

from data.base_data import BaseData
from data.util import file_utils
from . import excel_utils

import copy
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
                    self.set_column_index(sheet.name, columns)
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

        format_header = workbook.add_format({
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
            'right_color': '#666666',
            'align': 'left'
        })

        default_dict = {
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
            'right_color': '#666666',
            'align': 'left'
        }

        date_dict = copy.deepcopy(default_dict)
        date_dict['num_format'] = 'yyyy-mm-dd'
        date_dict['align'] = 'center'

        float_dict = copy.deepcopy(default_dict)
        float_dict['align'] = 'right'

        integer_dict = copy.deepcopy(default_dict)
        integer_dict['align'] = 'right'

        format_default = workbook.add_format(default_dict)
        format_date = workbook.add_format(date_dict)
        format_float = workbook.add_format(float_dict)
        format_integer = workbook.add_format(integer_dict)

        for data_key in self.get_data_keys():
            worksheet = workbook.add_worksheet(data_key)
            worksheet.freeze_panes(1, 0)
            worksheet.hide_gridlines(2)

            column_names = []

            row_idx = 0
            for col_idx, value in enumerate(self.get_columns(data_key)):
                column_names += [value]
                worksheet.write(row_idx, col_idx, value, format_header)

            data = self.get_data(data_key)
            for row_data in data:
                row_idx += 1
                for col_idx, value in enumerate(row_data):
                    cell_format = format_default
                    if col_idx < len(column_names):
                        column_name = column_names[col_idx]
                        column_info = self.get_column_info(data_key, column_name)
                        if column_info['type'] == 'date':
                            cell_format = format_date
                        elif column_info['type'] == 'float':
                            cell_format = format_float
                        elif column_info['type'] == 'integer':
                            cell_format = format_integer

                    worksheet.write(row_idx, col_idx, value, cell_format)

            worksheet.autofit()

        workbook.close()
