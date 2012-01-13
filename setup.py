#!/usr/bin/env python
# -*- coding: utf-8 -*-


from distutils.core import setup

from cardboard import __version__


with open("README.rst") as f:
    long_description = f.read()


setup(
    name="cardboard",
    version=__version__,
    author="Julian Berman",
    author_email="Julian+Cardboard@GrayVines.com",
    description="A Magic: The Gathering game engine",
    license="MIT/X",
    url="http://github.com/Julian/Cardboard",
    long_description = long_description,
    scripts=["bin/cardboard"],

    packages=[
        "cardboard",
        "cardboard.integration_tests",
        "cardboard.tests",

        "cardboard.cards",
        "cardboard.cards.tests",
        "cardboard.cards.sets",
        "cardboard.cards.sets.tests",

        "cardboard.db",
        "cardboard.db.tests",

        "cardboard.frontend",
        "cardboard.frontend.tests",
    ],

    install_requires=[
        "Minerva",
        "SQLAlchemy",
        "Twisted",
        # "jinja2",
        "jsonschema",
        # "mock",
        "panglery",
        "urwid >= 1.0.2",
        "zope.interface",
    ],
)
