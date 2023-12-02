from setuptools import find_packages, setup


setup(
    name='excel-to-csv',
    version='1.0',
    description='Convert excel file to cvs files sheet by sheet',
    license='MIT',
    author='Kyongho Lee',
    author_email='95116876+meta205@users.noreply.github.com',
    url='https://github.com/meta205/data-conversion-tools/',
    zip_safe=True,
    long_description=open('README.rst').read(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines()
)
