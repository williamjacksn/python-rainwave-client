import album
import song


class RainwaveArtist(object):

    simple_properties = [u'id', u'name']

    def __init__(self, channel, raw_info):
        self._channel = channel
        self._raw_info = raw_info

    def __getattr__(self, name):
        if name in self.simple_properties:
            return self._raw_info[u'artist_{}'.format(name)]
        else:
            raise AttributeError

    @property
    def numsongs(self):
        if u'artist_numsongs' not in self._raw_info:
            more_info = self._channel._get_artist_raw_info(self.id)
            self._raw_info = dict(self._raw_info.items() + more_info.items())
        return self._raw_info[u'artist_numsongs']

    @property
    def songs(self):
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

# channel -> artist_list -> artist
## numsongs, id, name
# channel -> album -> song -> artist
## id, lastplayed, name
