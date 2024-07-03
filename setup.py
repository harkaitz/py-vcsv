# -*- coding: utf-8 -*-
from distutils.core import setup
import os

with open('README.md') as f:
    README = f.read()

with open('COPYING') as f:
    LICENSE = f.read()

setup(
    name='vcsv',
    version='0.1',
    python_requires='>3.5.2',
    description='',
    long_description=README,
    author='Harkaitz Agirre',
    author_email='harkaitz.aguirre@gmail.com',
    url='https://github.com/harkaitz/py-vcsv',
    license=LICENSE,
    packages=['vcsv'],
    classifiers=[''],
    entry_points = {
        'console_scripts': [
            'vcsv = vcsv:vcsv_main',
        ],
    })
