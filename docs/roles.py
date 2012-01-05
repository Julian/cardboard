"""
Defines the custom roles used in Cardboard's documentation.

"""

import urllib

from docutils import nodes


def card_role(name, rawtext, text, lineno, inliner, options=None):
    """
    Link to a card in the Gatherer DB.

    """

    if options is None:
        options = {}

    app = inliner.document.settings.env.app
    node = card_node(rawtext, app, text, options)
    return [node], []


def card_node(rawtext, app, slug, options):
    """
    Make a card node for insertion into the document.

    """

    base = getattr(app.config, "card_db_url", None)
    if base is None:
        raise ValueError(
            "'card_db_url' is not properly set in the configuration (was %s)"
            % (base,)
        )
    uri = base.format(name=urllib.quote_plus(slug))
    return nodes.reference(rawtext, slug, refuri=uri, **options)


def setup(app):
    """
    Install the plugin.

    """

    app.add_role("card", card_role)
    app.add_config_value("card_db_url", None, "env")
