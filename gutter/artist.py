import album
import song


class RainwaveArtist(object):
    '''A :class:`RainwaveArtist` object represents one artist.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.artists` or
        :attr:`RainwaveSong.artists`.

    :param channel: the parent :class:`RainwaveChannel` object.
    :param raw_info: a dictionary of information provided by the API that
        describes the artist.'''

    def __init__(self, channel, raw_info):
        self._channel = channel
        self._raw_info = raw_info

    def __repr__(self):
        return u'RainwaveArtist({})'.format(self.name).encode(u'utf-8')

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
            more_info = self._channel._get_artist_raw_info(self.id)
            self._raw_info = dict(self._raw_info.items() + more_info.items())
        return self._raw_info[u'artist_numsongs']

    @property
    def songs(self):
        '''A list of :class:`RainwaveSong` objects attributed to the artist.'''
        if u'songs' not in self._raw_info:
            more_info = self._channel._get_artist_raw_info(self.id)
            self._raw_info = dict(self._raw_info.items() + more_info.items())
        if not hasattr(self, u'_songs'):
            self._songs = []
            for raw_song in self._raw_info[u'songs']:
                album_id = raw_song[u'album_id']
                new_raw_album = self._channel._get_album_raw_info(album_id)
                new_album = album.RainwaveAlbum(self._channel, new_raw_album)
                new_song = song.RainwaveSong(new_album, raw_song)
                self._songs.append(new_song)
        return self._songs
