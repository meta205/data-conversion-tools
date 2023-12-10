# -*- coding: utf-8 -*-

from data.base_data import BaseData
from . import excel_utils as utils

import os
import xlrd


class ExcelData(BaseData):
    def __init__(self, filename):
        super().__init__(os.path.split(filename)[0])
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
                        if cell_type == utils.XL_CELL_DATE:
                            cell_type = utils.XL_CELL_TIMESTAMP

                        if columns is not None:
                            column_info = self.get_column_info(sheet.name, columns[col_idx])
                            if column_info is not None:
                                cell_type = utils.to_cell_type(column_info['type'])

                        new_values += [utils.to_value(sheet, cell_type, old_values[col_idx])]

                    self.add_data(sheet.name, new_values)
