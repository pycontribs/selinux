#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages
from setuptools import setup
import warnings


warnings.filterwarnings(
    'ignore',
    "Unknown distribution option: 'long_description_content_type'",
    UserWarning)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Sorin Sbarnea",
    author_email='sorin.sbarnea@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="shim selinux module",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/plain; charset=UTF-8",
    include_package_data=True,
    keywords='selinux',
    name='selinux',
    packages=find_packages(include=['selinux']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pycontribs/selinux',
    version='0.1.4',
    zip_safe=False,
    data_files=[("", ["LICENSE"])],
)
