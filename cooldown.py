class RainwaveCooldownGroup(object):

    def __init__(self, channel, id, name):
        self._channel = channel
        self.id = id
        self.name = name

    def __repr__(self):
        attrs = {}
        attrs[u'channel'] = self._channel
        attrs[u'id'] = self.id
        attrs[u'name'] = self.name.__repr__()
        return u'RainwaveCooldownGroup({channel}, {id}, {name})'.format(**attrs)
