# -*- coding: utf-8 -*-

import json
import os


class BaseSchema(object):
    def __init__(self, schema_dir):
        json_file = open(os.path.join(schema_dir, '.schema.json'))
        self.schema_data = json.load(json_file)
        json_file.close()

    def get_column_info(self, object_name, column_name):
        object_info_dict = self.schema_data['objects']
        if object_name in object_info_dict:
            column_infos = object_info_dict[object_name]['columns']
            for column_info in column_infos:
                if column_name == column_info['name']:
                    return column_info

        return None
