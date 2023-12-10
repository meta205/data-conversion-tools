# -*- coding: utf-8 -*-

from data.excel.excel_data import ExcelData

import click

@click.group()
def data():
    pass


@data.command()
@click.argument('query')
@click.option('--path')
@click.option('--source', default='excel', type=click.Choice(['excel', 'json'], case_sensitive=False))
def select(query, source, path):
    if source == 'excel':
        excel_data = ExcelData(path)
        excel_data.read()
        excel_data.select(query)


@click.group()
def conversion():
    pass


cli = click.CommandCollection(sources=[data, conversion])

if __name__ == '__main__':
    cli()
