# -*- coding: utf-8 -*-

from .base_schema import BaseSchema
from data.util import query_utils

import csv
import os
import pandas as pd


class BaseData(object):
    def __init__(self, schema_dir):
        self.columns_dict = {}
        self.data_dict = {}

        self.base_schema = BaseSchema(schema_dir)

    def get_columns(self, data_key):
        if data_key in self.columns_dict:
            return self.columns_dict[data_key]
        return None

    def get_column_info(self, object_name, column_name):
        return self.base_schema.get_column_info(object_name, column_name)

    def set_columns(self, data_key, columns):
        self.columns_dict[data_key] = columns

    def get_data_keys(self):
        return sorted(list(self.columns_dict.keys()))

    def get_data(self, data_key):
        if data_key in self.data_dict:
            return self.data_dict[data_key]
        return []

    def add_data(self, data_key, row_data):
        if data_key not in self.data_dict:
            self.data_dict[data_key] = [row_data]
        else:
            self.data_dict[data_key] += [row_data]

    def select(self, query):
        final_df = None

        new_queries = [q.strip() for q in query.split('|')]
        for new_query in new_queries:
            data_key, columns = query_utils.get_query_info(new_query)
            if data_key is None:
                continue

            if data_key not in self.columns_dict:
                continue

            all_columns = self.columns_dict[data_key]
            if len(columns) == 0:
                columns = all_columns

            column_indexes = [all_columns.index(c) for c in columns]
            column_data_dict = {}

            data = self.data_dict[data_key]
            for row in data:
                for column_index in column_indexes:
                    if column_index < 0:
                        continue

                    column = all_columns[column_index]
                    if column not in column_data_dict:
                        column_data_dict[column] = [row[column_index]]
                    else:
                        column_data_dict[column] += [row[column_index]]

            final_df = pd.DataFrame(column_data_dict)

        print(final_df)
        return final_df

    def to_csv(self, csv_dir=None, exclude_empty_data=False):
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)

        for key in self.get_data_keys():
            exists_data = key in self.data_dict
            if exclude_empty_data and not exists_data:
                continue

            csv_file = open(os.path.join(csv_dir, '%s.csv' % key), 'w', newline='')

            writer = csv.writer(csv_file)
            writer.writerow(self.columns_dict[key])

            if not exists_data:
                csv_file.close()
                continue

            for values in self.data_dict[key]:
                writer.writerow(values)

            csv_file.close()
