import ConfigParser
import os
import sys
import platform


OS = platform.system()

if OS == "Darwin":
    APP_DATA = os.path.expanduser("~/Library/Application Support/Cardboard/")
    USER_DATA = os.path.expanduser("~/Library/Cardboard")
elif OS == "Windows":
    # XXX
    APP_DATA = "{[APPDATA]}/Cardboard/".format(os.environ)
    USER_DATA = "{[APPDATA]}/Cardboard/".format(os.environ)
else:
    APP_DATA = os.path.expanduser("~/.cardboard/")
    USER_DATA = os.path.expanduser("~/.cardboard/")

DEFAULTS = {
    "general" : {
        "auto_pay" : True,             # auto-pay costs when unambiguous
        "auto_tap" : True,             # auto-tap cards to pay costs
        "auto_single_select" : True,   # auto-perform trivial selections
        "unimplemented" : "quit",      # what to do for unimplemented cards
                                       # quit / manual_mode / remove
        "reorder_selections" : False,  # ask to reorder cards after a selection
        "splash" : True,               # show splash screen on start
    },

    "urwid" : {
        "C-t" : "turn",                # modify turn options for upcoming phase
    },

    "turn" : {
        "untap" : "skip",              # skip / auto / stop
        "upkeep" : "skip",
        "draw" : "skip",

        "first_main" : "stop",

        "beginning_combat" : "skip",   # skip / auto / attackers / stop
        "declare_attackers" : "attackers",
        "declare_blockers" : "attackers",
        "combat_damage" : "skip",
        "end_of_combat" : "skip",

        "second_main" : "stop",

        "cleanup" : "skip",
        "end" : "skip",
    },
}


def get(configparser, section, option, *args, **kwargs):
    """
    Get an option from a ConfigParser section.

    """

    # ConfigParser somehow manages to not support .get()ting from a config that
    # does not necessarily contain all the sections?

    try:
        return configparser.get(section, option, *args, **kwargs)
    except ConfigParser.NoSectionError as e:
        exc_info = sys.exc_info()

        try:
            return configparser.defaults()[section][option]
        except KeyError:
            pass

        raise e, exc_info[1], exc_info[2]


def load_config(config_file=None):
    config = ConfigParser.RawConfigParser(DEFAULTS)

    if config_file is None:
        config.read(os.path.join(APP_DATA, "config"))
    else:
        config.readfp(config_file)

    return config
