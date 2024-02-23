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

        self.object_names = []
        if 'objects' in self.schema_data:
            for key in self.schema_data['objects'].keys():
                self.object_names += [key]

        self.valid = True

    def get_object_names(self):
        return self.object_names

    def get_replace_object_name(self, object_name):
        if 'replace-names' not in self.schema_data:
            return object_name

        replace_name_dict = self.schema_data['replace-names']
        if object_name not in replace_name_dict:
            return object_name

        return replace_name_dict[object_name]

    def get_replace_column_name(self, object_name, column_name):
        if 'replace-names' not in self.schema_data:
            return column_name

        replace_name_dict = self.schema_data['replace-names']

        key = '%s.%s' % (object_name, column_name)
        if key not in replace_name_dict:
            return column_name

        split_values = replace_name_dict[key].split('.')
        if len(split_values) < 2:
            return column_name

        return split_values[1]

    def is_valid(self):
        return self.valid

    def has_object(self, object_name):
        if 'objects' in self.schema_data:
            object_info_dict = self.schema_data['objects']
            if object_name in object_info_dict:
                return True

        return False

    def get_columns(self, object_name):
        columns = []
        if 'objects' not in self.schema_data:
            return columns

        object_info_dict = self.schema_data['objects']
        if object_name in object_info_dict:
            column_infos = object_info_dict[object_name]['columns']
            for column_info in column_infos:
                columns += [column_info['name']]

        return columns

    def get_column_info(self, object_name, column_name):
        if 'objects' not in self.schema_data:
            return None

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

        default_value = None
        if 'default' in column_info:
            default_value = column_info['default']

        if column_type == 'boolean':
            if default_value is not None and default_value == 'true':
                return 'TRUE'
            return 'FALSE'
        elif column_type == 'float':
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
