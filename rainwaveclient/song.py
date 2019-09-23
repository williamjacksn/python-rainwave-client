from __future__ import unicode_literals

from . import category


class RainwaveSong(dict):
    """A :class:`RainwaveSong` object represents one song.

    .. note::

        You should not instantiate an object of this class directly, but rather obtain one from
        :attr:`RainwaveAlbum.songs`, :attr:`RainwaveArtist.songs`, or some other object.
    """

    def __init__(self, album, raw_info):
        self._album = album
        super(RainwaveSong, self).__init__(raw_info)

    def __len__(self):
        return self['length']

    def __repr__(self):
        return '<RainwaveSong [{0}]>'.format(self)

    def __str__(self):
        msg = '{0} // {1} // {2}'
        return msg.format(self.album, self.title, self.artist_string)

    @property
    def album(self):
        """The :class:`RainwaveAlbum` object the song belongs to."""
        return self._album

    @property
    def artist_string(self):
        """A single string with the names of all artists for the song."""
        return ', '.join([artist.name for artist in self.artists])

    @property
    def artists(self):
        """A list of :class:`RainwaveArtist` objects the song is attributed to."""
        if 'artist_objects' not in self:
            self['artist_objects'] = []
            if 'artists' not in self:
                song_obj = self.album.channel.get_song_by_id(self.id)
                self['artists'] = song_obj['artists']
            for raw_artist in self['artists']:
                artist_id = raw_artist['id']
                channel = self.album.channel
                new_artist = channel.get_artist_by_id(artist_id)
                self['artist_objects'].append(new_artist)
        return self['artist_objects']

    @property
    def available(self):
        """A boolean representing whether the song is available to play or not. Opposite of :attr:`cool`."""
        return not self.cool

    @property
    def categories(self):
        """A list of :class:`RainwaveCategory` objects representing the categories the song belongs to."""
        if 'category_objects' not in self:
            self['category_objects'] = []
            for raw_cat in self['groups']:
                chan = self.album.channel
                cat_id = raw_cat['id']
                name = raw_cat['name']
                cat = category.RainwaveCategory(chan, cat_id, name)
                self['category_objects'].append(cat)
        return self['category_objects']

    @property
    def channel_id(self):
        """The :attr:`RainwaveChannel.id` of the channel the song belongs to."""
        return self['sid']

    @property
    def cool(self):
        """A boolean representing whether the song is on cooldown. Opposite of :attr:`available`."""
        return self['cool']

    @property
    def fave(self):
        """A boolean representing whether the song is marked as a fave or not. Change whether the song is a fave by
        assigning a boolean value to this attribute."""
        return self['fave']

    @fave.setter
    def fave(self, value):
        value = bool(value)
        if value == self.fave:
            return
        d = self.album.channel.fave_song(self.id, str(value).lower())
        if d['fave_song_result']['success']:
            self['fave'] = value
        else:
            raise Exception(d['fave_song_result']['text'])

    @property
    def id(self):
        """The ID of the song."""
        return self['id']

    @property
    def length(self):
        """The length of the song in seconds. :class:`RainwaveSong` objects also support `len(song)`."""
        return len(self)

    @property
    def link_text(self):
        """The link text that corresponds with :attr:`url`."""
        return self['link_text']

    @property
    def origin_channel_id(self):
        """The :attr:`RainwaveChannel.id` of the home channel for the song. This could be different from
        :attr:`channel_id` if the song is in the playlist of multiple channels."""
        return self['origin_sid']

    @property
    def origin_sid(self):
        """See :attr:`origin_channel_id`."""
        return self.origin_channel_id

    @property
    def rating(self):
        """The rating given to the song by the listener authenticating to the API. Change the rating by assigning a new
        value to this attribute."""
        return self['rating_user']

    @rating.setter
    def rating(self, value):
        if self.rating == value:
            return
        d = self.album.channel.rate(self.id, value)
        if d['rate_result']['success']:
            self['rating_user'] = value
        else:
            raise Exception(d['rate_result']['text'])

    @rating.deleter
    def rating(self):
        d = self.album.channel.clear_rating(self.id)
        if d['rate_result']['success']:
            self['rating_user'] = None
        else:
            raise Exception(d['rate_result']['text'])

    @property
    def rating_allowed(self):
        """A boolean representing whether the listener can currently rate the song."""
        return self['rating_allowed']

    @property
    def rating_avg(self):
        """The average of all ratings given to the song by all listeners."""
        return self['rating']

    @property
    def rating_count(self):
        """The total number of ratings given to the song by all listeners."""
        return self['rating_count']

    @property
    def rating_histogram(self):
        """A dictionary representing the distribution of ratings given to the song by all listeners.
        For example::

            >>> song.rating_histogram
            {'1.0': 4, '1.5': 4, '2.0': 6, ..., '4.5': 46, '5.0': 26}
        """
        return self['rating_histogram']

    @property
    def rating_rank(self):
        """The position of the album when albums on the channel are ranked by rating. The highest-rated album will have
        :attr:`rating_rank` == 1."""
        return self['rating_rank']

    @property
    def rating_user(self):
        """See :attr:`rating`."""
        return self.rating

    @property
    def request_count(self):
        """The total number of times the song has been requested by any listener."""
        return self['request_count']

    @property
    def request_rank(self):
        """The position of the song when songs on the channel are ranked by how often they are requested. The
        most-requested song will have :attr:`rating_rank` == 1."""
        return self['rating_rank']

    @property
    def sid(self):
        """See :attr:`channel_id`."""
        return self.channel_id

    @property
    def title(self):
        """The title of the song."""
        return self['title']

    @property
    def url(self):
        """The URL of more information about the song."""
        return self['url']

    def request(self):
        """Add the song to the authenticating listener's request queue."""
        self.album.channel.request_song(self.id)


class RainwaveCandidate(RainwaveSong):
    """A :class:`RainwaveCandidate` object is a subclass of :class:`RainwaveSong` representing a song that is a
    candidate in an election."""

    def __init__(self, album, raw_info):
        super(RainwaveCandidate, self).__init__(album, raw_info)

    def __repr__(self):
        return '<RainwaveCandidate [{0}]>'.format(self)

    @property
    def entry_id(self):
        """The election entry ID for this candidate. Used for voting."""
        return self['entry_id']

    @property
    def is_request(self):
        """A boolean representing whether the candidate is a listener request or not."""
        return self['elec_request_user_id'] > 0

    @property
    def requested_by(self):
        """The :class:`RainwaveListener` who requested the candidate, if the candidate is a request. ``None``
        otherwise."""
        if self.is_request:
            user_id = self['elec_request_user_id']
            return self.album.channel.get_listener_by_id(user_id)
        return None

    def vote(self):
        """Cast a vote for the candidate."""
        d = self.album.channel.vote(self.entry_id)
        if not d['vote_result']['success']:
            raise Exception(d['vote_result']['text'])

    @property
    def votes(self):
        """The number of votes this candidate received in the election. If the election has not ended, :attr:`votes`
        will be ``0``."""
        return self['entry_votes']
