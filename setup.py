# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='data-conversion-tools',
    version='1.0',
    description='Data Conversion Tools',
    license='MIT',
    author='Kyongho Lee',
    author_email='meta205@naver.com',
    url='https://github.com/meta205/data-conversion-tools/',
    zip_safe=True,
    long_description=open('README.rst').read(),
    include_package_data=True,
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines()
)
