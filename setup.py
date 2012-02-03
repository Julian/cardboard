#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from cardboard import __version__


with open("README.rst") as f:
    long_description = f.read()


setup(
    name="cardboard",
    version=__version__,
    author="Julian Berman",
    author_email="Julian+Cardboard@GrayVines.com",
    description="A Magic: The Gathering game engine",
    long_description = long_description,
    license="MIT/X",
    url="http://github.com/Julian/Cardboard",
    packages=find_packages(),
    scripts=["bin/cardboard"],
    include_package_data=True,
    install_requires=[
        "Minerva",
        "SQLAlchemy",
        "Twisted",
        "jinja2",
        "jsonschema",
        "mock",
        "panglery",
        "txjsonrpc-tcp",
    ],
)
