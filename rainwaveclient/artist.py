from __future__ import unicode_literals


class RainwaveArtist(dict):
    """A :class:`RainwaveArtist` object represents one artist.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.artists` or
        :attr:`RainwaveSong.artists`.
    """

    def __init__(self, channel, raw_info):
        self._channel = channel
        super(RainwaveArtist, self).__init__(raw_info)

    def __repr__(self):
        return '<RainwaveArtist [{0}]>'.format(self)

    def __str__(self):
        return self.name

    @property
    def channel(self):
        """The :class:`RainwaveChannel` object associated with the artist."""
        return self._channel

    @property
    def id(self):
        """The ID of the artist."""
        return self['id']

    @property
    def name(self):
        """The name of the artist."""
        return self['name']

    @property
    def song_count(self):
        """The number of songs attributed to the artist."""
        return len(self.songs)

    @property
    def songs(self):
        """A list of :class:`RainwaveSong` objects attributed to the artist."""
        if 'song_objects' not in self:
            self['song_objects'] = []
            for chan_id, albums in self['all_songs'].items():
                for album_id, album_songs in albums.items():
                    for raw_song in album_songs:
                        song = self.channel.get_song_by_id(raw_song['id'])
                        self['song_objects'].append(song)
        return self['song_objects']
