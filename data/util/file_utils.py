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


def exists(path):
    return os.path.exists(path)


def is_dir(path):
    return os.path.isdir(path)


def make_dirs(path):
    if exists(path):
        return

    try:
        os.makedirs(path)
    except OSError:
        if not is_dir(path):
            raise


def find_files(dirname, postfix=None, ext=None):
    target_files = []

    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            fullpath = os.path.join(dirname, filename)
            if is_dir(fullpath):
                target_files += find_files(fullpath, postfix, ext)
            else:
                file_path, file_ext = os.path.splitext(fullpath)
                if postfix is not None and not file_path.endswith(postfix):
                    continue

                if ext is not None and file_ext != ('.' + ext):
                    continue

                target_files += [fullpath]
    except:
        pass

    return target_files
