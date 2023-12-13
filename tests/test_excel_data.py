# -*- coding: utf-8 -*-

import datetime
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

    def test_excel_data_select(self):
        excel_data = ExcelData(os.path.join('..', 'sample', 'SuperStoreUS-2015.xls'))
        excel_data.read()

        df = excel_data.select('orders[row_id, order_priority, customer_name, ship_mode, product_base_margin, order_date, quantity_ordered_new]')
        first_row = df.head(1).to_dict()

        self.assertEqual(first_row['row_id'], { 0: '20847' })
        self.assertEqual(first_row['order_priority'], { 0: 'High' })
        self.assertEqual(first_row['customer_name'], { 0: 'Bonnie Potter' })
        self.assertEqual(first_row['ship_mode'], { 0: 'Express Air' })
        self.assertEqual(first_row['product_base_margin'], { 0: 0.54 })
        self.assertEqual(first_row['order_date'], { 0: datetime.datetime(2015, 1, 7) })
        self.assertEqual(first_row['quantity_ordered_new'], { 0: 4 })
