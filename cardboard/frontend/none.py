class NoFrontend(object):
    def __init__(self, player, debug=False):
        super(NoFrontend, self).__init__()

        self.debug = debug

        self.game = player.game
        self.player = player

    def __repr__(self):
        return "<No Frontend Connected>"

    def priority_granted(self):
        pass

    def prompt(self, msg, *args, **kwargs):
        pass

    def select(self, choices, how_many=1, duplicates=False):
        return []
