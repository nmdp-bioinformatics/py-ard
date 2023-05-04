#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    py-ard
#    Copyright (c) 2023 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().split("\n")

with open("requirements-tests.txt") as requirements_file:
    test_requirements = requirements_file.read().split("\n")

setup(
    name="py-ard",
    version="1.0.0",
    description="ARD reduction for HLA with Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="CIBMTR",
    author_email="cibmtr-pypi@nmdp.org",
    url="https://github.com/nmdp-bioinformatics/py-ard",
    packages=[
        "pyard",
    ],
    provides=["pyard"],
    scripts=[
        "scripts/pyard",
        "scripts/pyard-import",
        "scripts/pyard-status",
        "scripts/pyard-reduce-csv",
    ],
    install_requires=requirements,
    license="LGPL 3.0",
    zip_safe=False,
    keywords="pyard",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    include_package_data=True,
)
