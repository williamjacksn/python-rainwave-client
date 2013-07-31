import datetime


class RainwaveSong(object):
    '''A :class:`RainwaveSong` object represents one song.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveAlbum.songs`,
        :attr:`RainwaveArtist.songs`, or some other object.
    '''

    #: The :class:`RainwaveAlbum` object the song belongs to.
    album = None

    def __init__(self, album, raw_info):
        self.album = album
        self._raw_info = raw_info

    def __repr__(self):
        # This is not a unicode literal because:
        # * str.format() automatically calls str() on self,
        # * __repr__() must return a string, not a unicode, and
        # * This library targets Python 2.7.
        return '<RainwaveSong [{}]>'.format(self)

    def __str__(self):
        # This is not a unicode literal because:
        # * __str__() must return a string, not a unicode.
        title = self.title.encode(u'utf-8')
        artist_string = self.artist_string.encode(u'utf-8')
        msg = '{} // {} // {}'
        return msg.format(self.album, title, artist_string)

    def _extend(self):
        for song in self.album.songs:
            if song.id == self.id:
                self._merge_raw_info(song)

    def _merge_raw_info(self, other):
        self._raw_info = dict(self._raw_info.items() + other._raw_info.items())

    @property
    def addedon(self):
        '''The UTC date and time the song was added to the playlist (a
        :class:`datetime.datetime` object).'''
        if u'song_addedon' not in self._raw_info:
            self._extend()
        ts = self._raw_info[u'song_addedon']
        return datetime.datetime.utcfromtimestamp(ts)

    @property
    def artist_string(self):
        '''A single string with the names of all artists for the song.'''
        return u', '.join([artist.name for artist in self.artists])

    @property
    def artists(self):
        '''A list of :class:`RainwaveArtist` objects the song is attributed
        to.'''
        if not hasattr(self, u'_artists'):
            self._artists = []
            if u'artists' not in self._raw_info:
                self._extend()
            for raw_artist in self._raw_info[u'artists']:
                artist_id = raw_artist[u'artist_id']
                channel = self.album.channel
                new_artist = channel.get_artist_by_id(artist_id)
                self._artists.append(new_artist)
        return self._artists

    @property
    def available(self):
        '''A boolean representing whether the song is available to play or
        not.'''
        if u'song_available' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_available']

    @property
    def channel_id(self):
        '''The :attr:`RainwaveChannel.id` of the channel the song belongs
        to.'''
        return self.album.channel.id

    @property
    def fav(self):
        '''See :attr:`favourite`.'''
        return self.favourite

    @property
    def favourite(self):
        '''A boolean representing whether the song is marked as a favourite or
        not. Change whether the song is a favourite by assigning a boolean
        value to this attribute.'''
        if u'song_favourite' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_favourite']

    @favourite.setter
    def favourite(self, value):
        value = bool(value)
        if value == self.favourite:
            return
        d = self.album.channel.fav_song(self.id, str(value).lower())
        if u'fav_song_result' in d:
            if d[u'fav_song_result'][u'code'] == 1:
                self._raw_info[u'song_favourite'] = value
            else:
                raise Exception(d[u'fav_song_result'][u'text'])
        else:
            raise Exception(d[u'error'][u'text'])

    @property
    def id(self):
        '''The ID of the song.'''
        return self._raw_info[u'song_id']

    @property
    def lastplayed(self):
        '''The UTC date and time the song last played (a
        :class:`datetime.datetime` object).'''
        if u'song_lastplayed' not in self._raw_info:
            self._extend()
        ts = self._raw_info[u'song_lastplayed']
        return datetime.datetime.utcfromtimestamp(ts)

    @property
    def rating(self):
        '''The rating given to the song by the listener authenticating to the
        API. Change the rating by assigning a new value to this attribute.'''
        if u'song_rating_user' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_rating_user']

    @rating.setter
    def rating(self, value):
        d = self.album.channel.rate(self.id, value)
        if u'rate_result' in d:
            if d[u'rate_result'][u'code'] == 1:
                self._raw_info[u'song_rating_user'] = value
            else:
                raise Exception(d[u'rate_result'][u'text'])
        else:
            raise Exception(d[u'error'][u'text'])

    @property
    def rating_avg(self):
        '''The average of all ratings given to the song by all listeners.'''
        if u'song_rating_avg' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_rating_avg']

    @property
    def rating_channel_id(self):
        '''The :attr:`RainwaveChannel.id` of the home channel for the song.
        This could be different from :attr:`channel_id` if the song is in the
        playlist of multiple channels.'''
        if u'song_rating_sid' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_rating_sid']

    @property
    def rating_count(self):
        '''The total number of ratings given to the song by all listeners.'''
        if u'song_rating_count' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_rating_count']

    @property
    def rating_id(self):
        '''The rating ID of the song. If a song appears on multiple channels,
        the :class:`RainwaveSong` objects will share a common :attr:`rating_id`
        so that when the song is rated on one channel the rating will be linked
        to the song on other channels.'''
        if u'song_rating_id' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_rating_id']

    @property
    def rating_sid(self):
        '''See :attr:`rating_channel_id`.'''
        return self.rating_channel_id

    @property
    def rating_user(self):
        '''See :attr:`rating`.'''
        return self.rating

    @property
    def releasetime(self):
        '''The UTC date and time the song will be out of cooldown and available
        to play. If the song is already available, :attr:`releasetime` will be
        in the past.'''
        if u'song_releasetime' not in self._raw_info:
            self._extend()
        ts = self._raw_info[u'song_releasetime']
        return datetime.datetime.utcfromtimestamp(ts)

    @property
    def secondslong(self):
        '''The length of the song in seconds.'''
        if u'song_secondslong' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_secondslong']

    @property
    def sid(self):
        '''See :attr:`channel_id`.'''
        return self.channel_id

    @property
    def timesdefeated(self):
        '''The number of times the song lost an election.'''
        if u'song_timesdefeated' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_timesdefeated']

    @property
    def timesplayed(self):
        '''The number of times the song has played.'''
        if u'song_timesplayed' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_timesplayed']

    @property
    def timeswon(self):
        '''The number of times the song won an election.'''
        if u'song_timeswon' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_timeswon']

    @property
    def title(self):
        '''The title of the song.'''
        if u'song_title' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_title']

    @property
    def totalrequests(self):
        '''The total number of times the song has been requested by any
        listener.'''
        if u'song_totalrequests' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_totalrequests']

    @property
    def totalvotes(self):
        '''The total number of election votes the song has received.'''
        if u'song_totalvotes' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_totalvotes']

    @property
    def url(self):
        '''The URL of more information about the song.'''
        if u'song_url' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_url']

    @property
    def urltext(self):
        '''The link text that corresponds with :attr:`url`.'''
        if u'song_urltext' not in self._raw_info:
            self._extend()
        return self._raw_info[u'song_urltext']

    def request(self):
        '''Add the song to the authenticating listener's request queue.'''
        self.album.channel.request_song(self.id)


class RainwaveCandidate(RainwaveSong):
    '''A :class:`RainwaveCandidate` object is a subclass of
    :class:`RainwaveSong` representing a song that is a candidate in an
    election.'''

    def __init__(self, album, raw_info):
        super(RainwaveCandidate, self).__init__(album, raw_info)

    def __repr__(self):
        return '<RainwaveCandidate [{}]>'.format(self)

    @property
    def conflicts_with(self):
        '''The :class:`RainwaveListener` who has a conflicting request, if the
        candidate is a conflict. :code:`None` otherwise.'''
        if self.isconflict:
            name = self._raw_info[u'song_requestor']
            return self.album.channel.get_listener_by_name(name)
        return None

    @property
    def elec_entry_id(self):
        '''The election entry ID for this candidate. Used for voting.'''
        return self._raw_info[u'elec_entry_id']

    @property
    def isconflict(self):
        '''A boolean representing whether the candidate conflicts with a
        listener's request.'''
        return self._raw_info[u'elec_isrequest'] in (0, 1)

    @property
    def isrequest(self):
        '''A boolean representing whether the candidate is a listener request
        or not.'''
        return self._raw_info[u'elec_isrequest'] in (3, 4)

    @property
    def requested_by(self):
        '''The :class:`RainwaveListener` who requested the candidate, if the
        candidate is a request. :code:`None` otherwise.'''
        if self.isrequest:
            name = self._raw_info[u'song_requestor']
            return self.album.channel.get_listener_by_name(name)
        return None

    @property
    def votes(self):
        '''The number of votes this candidate received in the election.'''
        return self._raw_info[u'elec_votes']

    def vote(self):
        '''Cast a vote for the candidate.'''
        d = self.album.channel.vote(self.elec_entry_id)
        if u'vote_result' in d:
            if d[u'vote_result'][u'code'] == 1:
                return
            else:
                raise Exception(d[u'vote_result'][u'text'])
        else:
            raise Exception(d[u'error'][u'text'])
