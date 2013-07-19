class RainwaveArtist(object):
    '''A :class:`RainwaveArtist` object represents one artist.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.artists` or
        :attr:`RainwaveSong.artists`.
    '''

    def __init__(self, channel, raw_info):
        self.channel = channel
        self._raw_info = raw_info

    def __repr__(self):
        return '<RainwaveArtist [{}]>'.format(self)

    def __str__(self):
        return self.name.encode(u'utf-8')

    @property
    def id(self):
        '''The ID of the artist.'''
        return self._raw_info[u'artist_id']

    @property
    def name(self):
        '''The name of the artist.'''
        return self._raw_info[u'artist_name']

    @property
    def numsongs(self):
        '''The number of songs attributed to the artist.'''
        if u'artist_numsongs' not in self._raw_info:
            more_info = self.channel._get_artist_raw_info(self.id)
            self._raw_info = dict(self._raw_info.items() + more_info.items())
        return self._raw_info[u'artist_numsongs']

    @property
    def songs(self):
        '''A list of :class:`RainwaveSong` objects attributed to the artist.'''
        if u'songs' not in self._raw_info:
            more_info = self.channel._get_artist_raw_info(self.id)
            self._raw_info = dict(self._raw_info.items() + more_info.items())
        if not hasattr(self, u'_songs'):
            self._songs = []
            for raw_song in self._raw_info[u'songs']:
                album_id = raw_song[u'album_id']
                album = self.channel.get_album_by_id(album_id)
                song_id = raw_song[u'song_id']
                song = album.get_song_by_id(song_id)
                self._songs.append(song)
        return self._songs
