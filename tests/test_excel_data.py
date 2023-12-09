import os
import unittest

from data.excel.excel_data import ExcelData


class ExcelDataTests(unittest.TestCase):
    """
    Excel data tests.
    """
    def test_excel_data_read(self):
        excel_data = ExcelData(os.path.join('..', 'sample', 'SuperStoreUS-2015.xls'))
        excel_data.read()

        self.assertEqual(excel_data.get_data_keys(), ['orders', 'returns', 'users'])
