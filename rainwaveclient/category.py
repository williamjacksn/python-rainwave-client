from __future__ import unicode_literals


class RainwaveCategory:

    def __init__(self, channel, category_id, name):
        self._channel = channel
        self.category_id = category_id
        self.name = name
