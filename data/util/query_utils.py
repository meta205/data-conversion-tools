# -*- coding: utf-8 -*-

import re


def get_query_info(query):
    """
    :param query:
    :return:
    """
    pattern = r'(?P<data_key>\w+)\[(?P<columns>[\w\s,]+)\]'
    result = re.match(pattern, query)

    data_key = result.group('data_key')
    if data_key is None:
        return None, None

    columns = result.group('columns')
    if columns is not None:
        columns = [c.strip() for c in columns.split(',')]
    else:
        columns = []

    return data_key, columns
