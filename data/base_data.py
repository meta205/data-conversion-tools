# -*- coding: utf-8 -*-

import csv
import os


class BaseData(object):
    def __init__(self):
        self.header_dict = {}
        self.data_dict = {}

    def add_header(self, key, header):
        self.header_dict[key] = header

    def add_data(self, key, values):
        if key not in self.data_dict:
            self.data_dict[key] = [values]
        else:
            self.data_dict[key] += [values]

    def get_data_keys(self):
        return list(self.header_dict.keys())

    def to_csv(self, csv_dir=None, exclude_empty_data=False):
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)

        csv_dirname = os.path.splitext(os.path.basename(csv_dir))[0]

        for key in self.get_data_keys():
            exists_data = key in self.data_dict
            if exclude_empty_data and not exists_data:
                continue

            csv_file = open(os.path.join(csv_dir, '%s.csv' % key), 'w', newline='')

            writer = csv.writer(csv_file)
            writer.writerow(self.header_dict[key])

            if not exists_data:
                csv_file.close()
                continue

            for values in self.data_dict[key]:
                writer.writerow(values)

            csv_file.close()
