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
            for row_idx in range(sheet.nrows):
                if row_idx == 0:
                    self.add_header(sheet.name, sheet.row_values(row_idx))
                else:
                    values = utils.convert_values(sheet, row_idx, sheet.row_values(row_idx))
                    self.add_data(sheet.name, values)
