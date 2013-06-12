import song


class RainwaveArtist(object):

    simple_properties = [u'id', u'name']

    extended_properties = [u'lastplayed', u'numsongs']

    def __init__(self, channel, raw_info):
        self._channel = channel
        self._raw_info = raw_info
        self._extended = False

    def __getattr__(self, name):
        if name in self.extended_properties:
            self._get_extended_properties()
        if name in self.simple_properties + self.extended_properties:
            return self._raw_info[u'artist_{}'.format(name)]
        else:
            raise AttributeError

    def _get_extended_properties(self):
        if not self._extended:
            _more_info = self._channel._get_artist_raw_info(self.id)
            self._raw_info = dict(self._raw_info.items() + _more_info.items())
            self._extended = True

    @property
    def songs(self):
        self._get_extended_properties()
        if not hasattr(self, u'_songs'):
            self._songs = []
            for raw_song in self._raw_info[u'songs']:
                album_id = raw_song[u'album_id']
                new_album = self._channel._get_album_raw_info(album_id)
                new_song = song.RainwaveSong(new_album, raw_song)
                self._songs.append(new_song)
        return self._songs

# channel -> artist_list -> artist
## numsongs, id, name
# channel -> album -> song -> artist
## id, lastplayed, name
