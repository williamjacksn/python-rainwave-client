import cooldown
import song


class RainwaveAlbum(object):

    simple_properties = [
        u'favourite',
        u'id',
        u'lowest_oa',
        u'name',
        u'rating_avg',
        u'rating_user'
    ]

    extended_properties = [
        u'fav_count',
        u'lastplayed',
        u'rating_count',
        u'rating_histogram',
        u'rating_rank',
        u'request_rank',
        u'timesdefeated',
        u'timesplayed',
        u'timesplayed_rank',
        u'timeswon',
        u'totalrequests',
        u'totalvotes',
        u'vote_rank'
    ]

    def __init__(self, channel, raw_info):
        self._channel = channel
        self._raw_info = raw_info
        self._extended = False

    def __getattr__(self, name):
        if name in self.extended_properties:
            self._get_extended_properties()
        if name in self.simple_properties + self.extended_properties:
            return self._raw_info[u'album_{}'.format(name)]
        else:
            raise AttributeError

    def _get_extended_properties(self):
        if not self._extended:
            self._raw_info = self._channel._get_album_raw_info(self.id)
            self._extended = True

    @property
    def art(self):
        self._get_extended_properties()
        base_url = self._channel._client.base_url
        return base_url + self._raw_info[u'album_art'].lstrip(u'/')

    @property
    def cooldown_groups(self):
        self._get_extended_properties()
        if not hasattr(self, u'_cooldown_groups'):
            self._cooldown_groups = []
            for raw_cdg in self._raw_info[u'album_genres']:
                id = raw_cdg[u'genre_id']
                name = raw_cdg[u'genre_name']
                cdg = cooldown.RainwaveCooldownGroup(self._channel, id, name)
                self._cooldown_groups.append(cdg)
        return self._cooldown_groups

    @property
    def fav(self):
        return self.favourite

    @property
    def songs(self):
        self._get_extended_properties()
        if not hasattr(self, u'_songs'):
            self._songs = []
            for raw_song in self._raw_info[u'song_data']:
                new_song = song.RainwaveSong(self, raw_song)
                self._songs.append(new_song)
        return self._songs
