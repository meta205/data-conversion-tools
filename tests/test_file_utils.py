# -*- coding: utf-8 -*-

import os
import unittest

from data.util import file_utils


class FileUtilsTests(unittest.TestCase):
    """
    File utils tests.
    """
    def test_new_filename(self):
        filename = os.path.join('..', 'sample', 'SuperStoreUS-2015.xls')
        new_filename = file_utils.new_filename(filename)

        self.assertEqual(new_filename, '../sample/SuperStoreUS-2015-new.xls')
