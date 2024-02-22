# -*- coding: utf-8 -*-

from data.excel.excel_data import ExcelData
from data.util import file_utils

import click


@click.group()
def data():
    pass


@data.command()
@click.argument('query')
@click.option('--source', default='excel', type=click.Choice(['excel', 'json'], case_sensitive=False))
@click.option('--path')
def select(query, source, path):
    if source == 'excel':
        excel_data = ExcelData(path)
        excel_data.read()
        excel_data.select(query)


@click.group()
def conversion():
    pass


@conversion.command()
@click.option('--path')
@click.option('--source', default='excel', type=click.Choice(['excel', 'json'], case_sensitive=False))
def newfile(source, path):
    if source == 'excel':
        if file_utils.is_dir(path):
            file_paths = file_utils.find_files(path, None, 'xls')
            for file_path in file_paths:
                excel_data = ExcelData(file_path)
                excel_data.read()
                excel_data.write()
        else:
            excel_data = ExcelData(path)
            excel_data.read()
            excel_data.write()


@conversion.command()
@click.option('--sql_dir')
@click.option('--path')
@click.option('--source', default='excel', type=click.Choice(['excel', 'json'], case_sensitive=False))
def tosql(source, path, sql_dir):
    if source == 'excel':
        excel_data = ExcelData(path)
        excel_data.read()
        excel_data.to_sql(sql_dir)


cli = click.CommandCollection(sources=[data, conversion])

if __name__ == '__main__':
    cli()
