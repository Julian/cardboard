class _ANY(object):
    def __eq__(self, other):
        return True

    def __repr__(self):
        return "<any>"

ANY = _ANY()
