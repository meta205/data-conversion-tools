# -*- coding: utf-8 -*-

from .base_schema import BaseSchema
from data.util import data_utils
from data.util import query_utils

import csv
import os
import pandas as pd


class BaseData(object):
    def __init__(self, schema_dir):
        self.columns_index_dict = {}
        self.columns_dict = {}
        self.data_dict = {}

        self.dest = None

        self.base_schema = BaseSchema(schema_dir)

    def get_dest(self):
        return self.dest

    def set_dest(self, dest):
        self.dest = dest

    def get_schema(self):
        return self.base_schema

    def get_columns(self, data_key):
        if data_key in self.columns_dict:
            return self.columns_dict[data_key]
        return None

    def get_column_info(self, table_name, column_name):
        return self.base_schema.get_column_info(table_name, column_name)

    def set_columns(self, data_key, columns):
        schema_columns = self.base_schema.get_columns(data_key)
        if len(schema_columns) == 0:
            self.columns_index_dict[data_key] = list(range(len(columns)))
            self.columns_dict[data_key] = columns
            return

        self.columns_index_dict[data_key] = [columns.index(c) if c in columns else -1 for c in schema_columns]
        self.columns_dict[data_key] = schema_columns

    def get_data_keys(self):
        return sorted(list(self.columns_dict.keys()))

    def get_data(self, data_key):
        if data_key in self.data_dict:
            return self.data_dict[data_key]
        return []

    def add_data(self, data_key, row_data):
        new_row_data = row_data
        if data_key in self.columns_index_dict:
            columns = self.columns_dict[data_key]
            column_indexes = self.columns_index_dict[data_key]

            new_row_data = []
            for idx, column_index in enumerate(column_indexes):
                if column_index < 0:
                    new_row_data += [self.base_schema.get_default_value(data_key, columns[idx])]
                else:
                    new_row_data += [row_data[column_index]]

        if data_key not in self.data_dict:
            self.data_dict[data_key] = [new_row_data]
        else:
            self.data_dict[data_key] += [new_row_data]

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

    def to_sql(self, sql_dir=None):
        if not os.path.exists(sql_dir):
            os.mkdir(sql_dir)

        for key in self.get_data_keys():
            if key not in self.data_dict:
                continue

            columns = self.get_columns(key)
            if columns is None:
                continue

            data = self.data_dict[key]
            if len(data) == 0:
                continue

            sql_file = open(os.path.join(sql_dir, '%s.sql' % key), 'w', newline='')

            for row in data:
                new_columns = ', '.join(columns)
                new_values = ', '.join([data_utils.to_string(columns[idx], col) for idx, col in enumerate(row)])

                sql_file.write(f'INSERT INTO {key.upper()} ({new_columns}) VALUES ({new_values});\n')

            sql_file.close()
