import artist


class RainwaveSong(object):

    simple_properties = [
        u'addedon',
        u'available',
        u'favourite',
        u'id',
        u'lastplayed',
        u'rating_avg',
        u'rating_count',
        u'rating_id',
        u'rating_sid',
        u'rating_user',
        u'releasetime',
        u'secondslong',
        u'timesdefeated',
        u'timesplayed',
        u'timeswon',
        u'title',
        u'totalrequests',
        u'totalvotes',
        u'url',
        u'urltext'
    ]

    def __init__(self, album, raw_info):
        self.album = album
        self._raw_info = raw_info

    def __getattr__(self, name):
        if name in self.simple_properties:
            if u'song_{}'.format(name) not in self._raw_info:
                for song in self.album.songs:
                    if song.id == self.id:
                        self._merge_raw_info(song)
            return self._raw_info[u'song_{}'.format(name)]
        else:
            raise AttributeError

    def _merge_raw_info(self, other):
        self._raw_info = dict(self._raw_info.items() + other._raw_info.items())

    @property
    def artists(self):
        if not hasattr(self, u'_artists'):
            self._artists = []
            if u'artists' not in self._raw_info:
                for song in self.album.songs:
                    if song.id == self.id:
                        self._merge_raw_info(song)
            for raw_artist in self._raw_info[u'artists']:
                channel = self.album._channel
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
