#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spackle import version

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='spackle',
    version=version.__version__,
    description="spack helpers",
    long_description=readme + '\n\n' + history,
    author="Tom Barron",
    author_email='tusculum@gmail.com',
    url='https://github.com/tbarron/spackle',
    packages=[
        'spackle',
    ],
    package_dir={'spackle': 'spackle'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='spack',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points = {'console_scripts': ["spackle = spackle:main"]},
)
