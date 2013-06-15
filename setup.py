# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='company-scraper',
    version=1.0,
    author='José Antonio Rubio Conesa',
    author_email='jarubc@gmail.com',
    packages=['linkedin', 'linkedin.spiders'],
    install_requires=[
        'Scrapy >= 0.16.5',
        'pymongo >= 2.5.2',
    ]
)
