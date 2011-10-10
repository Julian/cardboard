#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

from cardboard import __version__


long_description = (
"""*cardboard* is [yet another] Magic: The Gathering™ client, which at some
point will hopefully have things like:

    likely
    ------

    * multiplayer support
    * drafting
    * multiple frontends, including a <canvas> frontend

    slightly less likely
    --------------------

    * a simple AI

    pie in the sky
    --------------

    * MTGO-like collectability / economy

"""
)

setup(
    name="cardboard",
    version = __version__,
    author = "Julian Berman",
    author_email = "Julian+Cardboard@GrayVines.com",
    description = "cardboard is a Magic: The Gathering client",
    license = "MIT/X",
    url = "http://github.com/Julian/cardboard",
    long_description = long_description,
    packages = ["cardboard", "cardboard.cards", "cardboard.db",
                "cardboard.frontend", "cardboard.tests"],
    scripts = ["bin/cardboard"],
    install_requires = [
        "panglery",
        "twisted",
        "urwid >= 1.0.0",
    ],
)
