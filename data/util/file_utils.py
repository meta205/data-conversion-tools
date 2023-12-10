# -*- coding: utf-8 -*-

import os


def new_filename(file_path, suffix_name='-new'):
    file_name, file_extension = os.path.splitext(file_path)
    new_name = f'{file_name}{suffix_name}{file_extension}'

    seq = 0
    while os.path.exists(new_name):
        seq += 1
        new_name = f'{file_name}{suffix_name}{seq}{file_extension}'

    return new_name
