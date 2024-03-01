# -*- coding: utf-8 -*-

import json
import os


class BaseSchema(object):
    def __init__(self, schema_dir):
        schema_file = os.path.join(schema_dir, '.schema.json')
        if not os.path.exists(schema_file):
            self.schema_data = {}
            self.valid = False
            return

        json_file = open(schema_file)
        self.schema_data = json.load(json_file)
        json_file.close()

        self.table_names = []
        if 'tables' in self.schema_data:
            for key in self.schema_data['tables'].keys():
                self.table_names += [key]

        self.valid = True

    def get_table_names(self):
        return self.table_names

    def get_replace_table_name(self, table_name):
        if 'replace-names' not in self.schema_data:
            return table_name

        replace_name_dict = self.schema_data['replace-names']
        if table_name not in replace_name_dict:
            return table_name

        return replace_name_dict[table_name]

    def get_replace_column_name(self, table_name, column_name):
        if 'replace-names' not in self.schema_data:
            return column_name

        replace_name_dict = self.schema_data['replace-names']

        key = '%s.%s' % (table_name, column_name)
        if key not in replace_name_dict:
            return column_name

        split_values = replace_name_dict[key].split('.')
        if len(split_values) < 2:
            return column_name

        return split_values[1]

    def is_valid(self):
        return self.valid

    def has_table(self, table_name):
        if 'tables' in self.schema_data:
            object_info_dict = self.schema_data['tables']
            if table_name in object_info_dict:
                return True

        return False

    def get_columns(self, table_name):
        columns = []
        if 'tables' not in self.schema_data:
            return columns

        object_info_dict = self.schema_data['tables']
        if table_name in object_info_dict:
            column_infos = object_info_dict[table_name]['columns']
            for column_info in column_infos:
                columns += [column_info['name']]

        return columns

    def get_column_info(self, table_name, column_name):
        if 'tables' not in self.schema_data:
            return None

        object_info_dict = self.schema_data['tables']
        if table_name in object_info_dict:
            column_infos = object_info_dict[table_name]['columns']
            for column_info in column_infos:
                if column_name == column_info['name']:
                    return column_info

        return None

    def get_default_value(self, table_name, column_name):
        column_info = self.get_column_info(table_name, column_name)
        if column_info is None:
            return ''

        column_type = column_info['type']

        default_value = None
        if 'default' in column_info:
            default_value = column_info['default']

        if column_type == 'boolean':
            if default_value is not None and default_value == 'true':
                return 'TRUE'
            return 'FALSE'
        elif column_type == 'number':
            if default_value is not None and len(str(default_value)) > 0:
                return float(str(default_value))
            return '0.0'
        elif column_type == 'integer':
            if default_value is not None and len(str(default_value)) > 0:
                return int(str(default_value))
            return '0'

        if default_value is not None and len(str(default_value)) > 0:
            return str(default_value)

        return ''
