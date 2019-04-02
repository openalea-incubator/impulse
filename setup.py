#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from setuptools import setup, find_packages


short_descr = "belle petite description"
readme = open('README.rst').read()
history = open('HISTORY.rst').read()

# find packages
pkgs = find_packages('src')



setup_kwds = dict(
    name='impulse',
    version="0.0.1",
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="moi",
    author_email="moi@email.com",
    url='https://github.com/moi/impulse',
    license='cecill-c',
    zip_safe=False,

    packages=pkgs,
    package_dir={'': 'src'},
    setup_requires=[
        "pytest-runner",
        ],
    install_requires=[
        ],
    tests_require=[
        "pytest",
        "pytest-mock",
        ],
    entry_points={},
    keywords='',
    )
# #}
# change setup_kwds below before the next pkglts tag

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
