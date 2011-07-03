#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for pdf2zip."""

from setuptools import setup, find_packages
import sys, os

version = '0.1'

# some trove classifiers:

# License :: OSI Approved :: MIT License
# Intended Audience :: Developers
# Operating System :: POSIX

setup(
    name='pdf2zip',
    version=version,
    description="pdf conversion utility",
    long_description=open('README.rst').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    keywords='pdf to jpeg conversion',
    author='Jason Moiron',
    author_email='jmoiron@jmoiron.net',

    url='http://github.com/jmoiron/pdf2zip',
    license='MIT',
    packages=['pdf2zip'],
    scripts=['bin/pdf2zip'],
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    install_requires=[
      # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
