#!/usr/bin/env python
#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of pykiq
# (see https://github.com/carstencodes/pykiq).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages

__VERSION__ = "0.9.0"

long_description: str = ""
with open("README.md", "r") as read_me_file:
    long_description = read_me_file.read()

setup(
    name="pykiq",
    version=__VERSION__,
    license="LGPL-3.0-only",
    author="Carsten Igel",
    author_email="cig@bite-that-bit.de",
    description="A simple storage system for dataclasses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    url="https://github.com/carstencodes/dcstore",
    install_requires=["redis"],
    extras_require={},
    package_dir={"": "src"},
    keywords="sidekiq, job, development",
    python_requires=">=3.7, < 4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General"
        + " Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System",
        "Typing :: Typed",
    ],
)
