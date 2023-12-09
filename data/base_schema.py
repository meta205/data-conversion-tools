# -*- coding: utf-8 -*-

import json
import os


class BaseSchema(object):
    def __init__(self, schema_dir):
        json_file = open(os.path.join(schema_dir, '.schema.json'))
        self.schema_data = json.load(json_file)
        print(self.schema_data)
        json_file.close()
