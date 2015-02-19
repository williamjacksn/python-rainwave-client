import datetime

from . import cooldown
from . import song


class RainwaveAlbum(object):
    """A :class:`RainwaveAlbum` object represents one album.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.albums`.
    """

    #: The :class:`RainwaveChannel` object the album belongs to.
    channel = None

    def __init__(self, channel, raw_info):
        self.channel = channel
        self._raw_info = raw_info

    def __repr__(self):
        msg = '<RainwaveAlbum [{} // {}]>'
        return msg.format(self.channel.name, self.name)

    def __str__(self):
        msg = '{} // {}'
        return msg.format(self.channel.name, self.name)

    def _extend(self):
        self._raw_info = self.channel._get_album_raw_info(self.id)

    @property
    def art(self):
        """The URL of the cover art for the album."""
        if 'album_art' not in self._raw_info:
            self._extend()
        base_url = self.channel.client.base_url
        return base_url + self._raw_info['album_art'].lstrip('/')

    @property
    def cooldown_groups(self):
        """A list of :class:`RainwaveCooldownGroup` objects representing the
        cooldown groups the songs in the album belong to."""
        if 'album_genres' not in self._raw_info:
            self._extend()
        if not hasattr(self, '_cooldown_groups'):
            self._cooldown_groups = []
            for raw_cdg in self._raw_info['album_genres']:
                id = raw_cdg['genre_id']
                name = raw_cdg['genre_name']
                cdg = cooldown.RainwaveCooldownGroup(self.channel, id, name)
                self._cooldown_groups.append(cdg)
        return self._cooldown_groups

    @property
    def fav(self):
        """See :attr:`favourite`."""
        return self.favourite

    @property
    def fav_count(self):
        """The number of listeners who have marked the album as a favourite."""
        if 'album_fav_count' not in self._raw_info:
            self._extend()
        return self._raw_info['album_fav_count']

    @property
    def favourite(self):
        """A boolean representing whether the album is marked as a favourite or
        not. Change whether the album is a favourite by assigning a boolean
        value to this attribute."""
        return self._raw_info['album_favourite']

    @favourite.setter
    def favourite(self, value):
        value = bool(value)
        if value == self.favourite:
            return
        d = self.channel.fav_album(self.id, str(value).lower())
        if 'fav_album_result' in d:
            if d['fav_album_result']['code'] == 1:
                self._raw_info['album_favourite'] = value
            else:
                raise Exception(d['fav_album_result']['text'])
        else:
            raise Exception(d['error']['text'])

    @property
    def id(self):
        """The ID of the album."""
        return self._raw_info['album_id']

    @property
    def lastplayed(self):
        """A :class:`datetime.datetime` object specifying the most recent date
        and time when a song in the album played."""
        if 'album_lastplayed' not in self._raw_info:
            self._extend()
        ts = self._raw_info['album_lastplayed']
        return datetime.datetime.utcfromtimestamp(ts)

    @property
    def lowest_cd(self):
        """A :class:`datetime.datetime` object specifying the earliest date and
        time a song in the album will be out of cooldown and available to play.
        If any song in the album is already available, :attr:`lowest_cd` will
        be in the past."""
        ts = self._raw_info['album_lowest_oa']
        return datetime.datetime.utcfromtimestamp(ts)

    @property
    def lowest_oa(self):
        """See :attr:`lowest_cd`."""
        return self.lowest_cd

    @property
    def name(self):
        """The name of the album."""
        return self._raw_info['album_name']

    @property
    def rating(self):
        """The average of all ratings given to songs in the album by only the
        listener authenticating to the API."""
        return self._raw_info['album_rating_user']

    @property
    def rating_avg(self):
        """The average of all ratings given to songs in the album by all
        listeners."""
        return self._raw_info['album_rating_avg']

    @property
    def rating_count(self):
        """The total number of ratings given to songs in the album by all
        listeners."""
        if 'album_rating_count' not in self._raw_info:
            self._extend()
        return self._raw_info['album_rating_count']

    @property
    def rating_histogram(self):
        """A dictionary representing the distribution of ratings given to all
        songs in the album by all listeners. For example::

            >>> album.rating_histogram
            {'1.0': 4, '1.5': 4, '2.0': 6, ..., '4.5': 46, '5.0': 26}
        """
        if 'album_rating_histogram' not in self._raw_info:
            self._extend()
        return self._raw_info['album_rating_histogram']

    @property
    def rating_rank(self):
        """The position of the album when albums on the channel are ranked by
        rating. The highest-rated album will have :attr:`rating_rank` == 1."""
        if 'album_rating_rank' not in self._raw_info:
            self._extend()
        return self._raw_info['album_rating_rank']

    @property
    def rating_user(self):
        """See :attr:`rating`."""
        return self.rating

    @property
    def request_rank(self):
        """The position of the album when albums on the channel are ranked by
        how often they are requested. The most-requested album will have
        :attr:`request_rank` == 1."""
        if 'album_request_rank' not in self._raw_info:
            self._extend()
        return self._raw_info['album_request_rank']

    @property
    def songs(self):
        """A list of :class:`RainwaveSong` objects in the album."""
        self._extend()
        if not hasattr(self, '_songs'):
            self._songs = []
            for raw_song in self._raw_info['song_data']:
                new_song = song.RainwaveSong(self, raw_song)
                self._songs.append(new_song)
        return self._songs

    @property
    def timesdefeated(self):
        """The number of times a song in the album lost an election."""
        if 'album_timesdefeated' not in self._raw_info:
            self._extend()
        return self._raw_info['album_timesdefeated']

    @property
    def timesplayed(self):
        """The number of times a song in the album has played."""
        if 'album_timesplayed' not in self._raw_info:
            self._extend()
        return self._raw_info['album_timesplayed']

    @property
    def timesplayed_rank(self):
        """The position of the album when albums on the channel are ranked by
        how often they are played. The most-played album will have
        :attr:`timesplayed_rank` == 1."""
        if 'album_timesplayed_rank' not in self._raw_info:
            self._extend()
        return self._raw_info['album_timesplayed_rank']

    @property
    def timeswon(self):
        """The number of times a song in the album won an election."""
        if 'album_timeswon' not in self._raw_info:
            self._extend()
        return self._raw_info['album_timeswon']

    @property
    def totalrequests(self):
        """The total number of times a song in the album was requested by any
        listener."""
        if 'album_totalrequests' not in self._raw_info:
            self._extend()
        return self._raw_info['album_totalrequests']

    @property
    def totalvotes(self):
        """The total number of election votes songs in the album have
        received."""
        if 'album_totalvotes' not in self._raw_info:
            self._extend()
        return self._raw_info['album_totalvotes']

    @property
    def vote_rank(self):
        """The position of the album when albums on the channel are ranked by
        how many votes they received. The most-voted-for album will have
        :attr:`vote_rank` == 1."""
        if 'album_vote_rank' not in self._raw_info:
            self._extend()
        return self._raw_info['album_vote_rank']

    def get_song_by_id(self, id):
        """ Return a :class:`RainwaveSong` for the given song ID. Raises an
        :exc:`IndexError` if there is no song with the given ID in the
        album.

        :param id: the ID of the desired song.
        :type id: int
        """

        for song in self.songs:
            if song.id == id:
                return song
        raise IndexError('Album does not contain song with id: {}'.format(id))
