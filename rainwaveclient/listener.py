class RainwaveListener:
    """A :class:`RainwaveListener` object represents a radio listener."""

    #: The :class:`RainwaveChannel` the listener belongs to.
    channel = None

    def __init__(self, channel, raw_info):
        self.channel = channel
        self._raw_info = raw_info

    def __repr__(self):
        return '<RainwaveListener [{}]>'.format(self)

    def __str__(self):
        return self.name

    def _extend(self):
        more_info = self.channel._get_listener_raw_info(self.id)
        self._raw_info = dict(self._raw_info.items() + more_info.items())

    def _get_extended(self, name):
        if name not in self._raw_info:
            self._extend()
        return self._raw_info[name]

    @property
    def id(self):
        """The ID of the listener."""
        return self._raw_info['user_id']

    @property
    def losingrequests(self):
        """The number of requests made by the listener that lost their
        election."""
        return self._get_extended('radio_losingrequests')

    @property
    def losingvotes(self):
        """The number of votes the listeners has given to a song that lost an
        election."""
        return self._get_extended('radio_losingvotes')

    @property
    def name(self):
        """The name of the listener."""
        return self._raw_info['username']

    @property
    def topalbums(self):
        """A list of the ten :class:`RainwaveAlbum` objects that the listener
        has given the highest rating to."""
        _topalbums = []
        for album in self._get_extended('user_topalbums'):
            new_album = self.channel.get_album_by_name(album['album_name'])
            _topalbums.append(new_album)
        return _topalbums

    @property
    def totalmindchange(self):
        """The total number of times the listener changed a song rating."""
        return self._get_extended('radio_totalmindchange')

    @property
    def totalratings(self):
        """The total number of songs the listener has rated."""
        return self._get_extended('radio_totalratings')

    @property
    def votes(self):
        """The number of votes the listener has cast in the last two weeks."""
        return self._raw_info['radio_2wkvotes']

    @property
    def winningrequests(self):
        """The number of requests made by the listener that won their
        election."""
        return self._get_extended('radio_winningrequests')

    @property
    def winningvotes(self):
        """The number of votes the listener has given to a song that won an
        election."""
        return self._get_extended('radio_winningvotes')
