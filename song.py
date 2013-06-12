import artist


class RainwaveSong(object):

    simple_properties = [u'addedon', u'available', u'favourite', u'id',
        u'lastplayed', u'rating_avg', u'rating_count', u'rating_id',
        u'rating_sid', u'rating_user', u'releasetime', u'secondslong',
        u'timesdefeated', u'timesplayed', u'timeswon', u'title',
        u'totalrequests', u'totalvotes', u'url', u'urltext']

    def __init__(self, album, raw_info):
        self._album = album
        self._raw_info = raw_info
        for song in self._album.songs:
            if song.id == self.id:
                self._raw_info = dict(self._raw_info.items() + song._raw_info.items())

    def __getattr__(self, name):
        if name in self.simple_properties:
            return self._raw_info[u'song_{}'.format(name)]
        else:
            raise AttributeError

    @property
    def artists(self):
        if not hasattr(self, u'_artists'):
            self._artists = []
            for raw_artist in self._raw_info[u'artists']:
                channel = self._album._channel
                new_artist = artist.RainwaveArtist(channel, raw_artist)
                self._artists.append(new_artist)
        return self._artists

    @property
    def channel_id(self):
        return self.sid

    @property
    def fav(self):
        return self.favourite

    @property
    def rating_channel_id(self):
        return self.rating_sid

    @property
    def sid(self):
        return self._raw_info[u'sid']
