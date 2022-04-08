class RainwaveCategory:

    def __init__(self, channel, category_id, name):
        self._channel = channel
        self.category_id = category_id
        self.name = name

    def __repr__(self) -> str:
        return f'<RainwaveCategory [{self}]>'

    def __str__(self) -> str:
        return self.name
