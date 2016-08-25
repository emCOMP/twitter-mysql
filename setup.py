#!/usr/bin/env python

import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(req.req) for req in install_reqs]


setup(
    name='twitter_mysql',
    version='0.1',
    description='Scripts for normalizing a twitter dataset into mysql',
    author='John Robinson',
    author_email='soco@uw.edu',
    url='https://www.geosoco.com/projects/twitter-mysql/',
    packages=['twitter_mysql'],
    install_requires=reqs,
)
