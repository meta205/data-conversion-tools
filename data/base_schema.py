# -*- coding: utf-8 -*-

import json
import os


class BaseSchema(object):
    def __init__(self, schema_dir):
        json_file = open(os.path.join(schema_dir, '.schema.json'))
        self.schema_data = json.load(json_file)
        json_file.close()

    def get_columns(self, object_name):
        columns = []

        object_info_dict = self.schema_data['objects']
        if object_name in object_info_dict:
            column_infos = object_info_dict[object_name]['columns']
            for column_info in column_infos:
                columns += [column_info['name']]

        return columns

    def get_column_info(self, object_name, column_name):
        object_info_dict = self.schema_data['objects']
        if object_name in object_info_dict:
            column_infos = object_info_dict[object_name]['columns']
            for column_info in column_infos:
                if column_name == column_info['name']:
                    return column_info

        return None

    def get_default_value(self, object_name, column_name):
        column_info = self.get_column_info(object_name, column_name)
        if column_info is None:
            return ''

        column_type = column_info['type']
        if column_type == 'boolean':
            return 'FALSE'
        elif column_type == 'float':
            return '0.0'
        elif column_type == 'integer':
            return '0'

        return ''
