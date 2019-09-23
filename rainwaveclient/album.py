from __future__ import unicode_literals

import datetime

from . import category


class RainwaveAlbum(dict):
    """A :class:`RainwaveAlbum` object represents one album.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.albums`.
    """

    def __init__(self, channel, raw_info):
        self._channel = channel
        super(RainwaveAlbum, self).__init__(raw_info)

    def __repr__(self):
        _repr = '<RainwaveAlbum [{0} // {1}]>'
        return _repr.format(self.channel.name, self.name)

    def __str__(self):
        _str = '{0} // {1}'
        return _str.format(self.channel.name, self.name)

    @property
    def art(self):
        """The URL of the cover art for the album."""
        return self.channel.client.art_fmt.format(self['art'])

    @property
    def added_on(self):
        """A :class:`datetime.datetime` object specifying when the album was
        added to the playlist."""
        return datetime.datetime.utcfromtimestamp(self['added_on'])

    @property
    def categories(self):
        """A list of :class:`RainwaveCategory` objects representing the
        categories the songs in the album belong to."""
        if 'category_objects' not in self:
            self['category_objects'] = []
            for raw_cat in self['genres']:
                category_id = raw_cat['id']
                name = raw_cat['name']
                cat = category.RainwaveCategory(self.channel, category_id, name)
                self['category_objects'].append(cat)
        return self['category_objects']

    @property
    def channel(self):
        """The :class:`RainwaveChannel` object the album belongs to."""
        return self._channel

    @property
    def cool(self):
        """A boolean representing whether the entire album is on cooldown.
        :attr:`cool` will be `True` if and only if every song in the album is on
        cooldown."""
        return self['cool']

    @property
    def cool_lowest(self):
        """A :class:`datetime.datetime` object specifying the earliest date and
        time a song in the album will be out of cooldown and available to play.
        If any song in the album is already available, :attr:`cool_lowest` will
        be in the past."""
        return datetime.datetime.utcfromtimestamp(self['cool_lowest'])

    @property
    def fave(self):
        """A boolean representing whether the album is marked as a fave or not.
        Change whether the album is a fave by assigning a boolean value to this
        attribute."""
        return self.get('fave', False)

    @fave.setter
    def fave(self, value):
        value = bool(value)
        if value == self.fave:
            return
        d = self.channel.fave_album(self.id, str(value).lower())
        if d['fave_album_result']['success']:
            self['fave'] = value
        else:
            raise Exception(d['fave_album_result']['text'])

    @property
    def fave_count(self):
        """The number of listeners who have marked the album as a favourite."""
        return self['fave_count']

    @property
    def id(self):
        """The ID of the album."""
        return self['id']

    @property
    def name(self):
        """The name of the album."""
        return self['name']

    @property
    def played_last(self):
        """A :class:`datetime.datetime` object specifying the most recent date
        and time when a song in the album played."""
        return datetime.datetime.utcfromtimestamp(self['played_last'])

    @property
    def rating(self):
        """The average of all ratings given to songs in the album by only the
        listener authenticating to the API."""
        return self['rating_user']

    @property
    def rating_avg(self):
        """The average of all ratings given to songs in the album by all
        listeners."""
        return self['rating']

    @property
    def rating_complete(self):
        """A boolean representing whether the listener has rated all songs in
        the album."""
        return self['rating_complete']

    @property
    def rating_count(self):
        """The total number of ratings given to songs in the album by all
        listeners."""
        return self['rating_count']

    @property
    def rating_histogram(self):
        """A dictionary representing the distribution of ratings given to all
        songs in the album by all listeners. For example::

            >>> album.rating_histogram
            {'1.0': 4, '1.5': 4, '2.0': 6, ..., '4.5': 46, '5.0': 26}
        """
        return self['rating_histogram']

    @property
    def rating_rank(self):
        """The position of the album when albums on the channel are ranked by
        rating. The highest-rated album will have :attr:`rating_rank` == 1."""
        return self['rating_rank']

    @property
    def rating_user(self):
        """See :attr:`rating`."""
        return self.rating

    @property
    def request_count(self):
        """The total number of times a song in the album was requested by any
        listener."""
        return self['request_count']

    @property
    def request_rank(self):
        """The position of the album when albums on the channel are ranked by
        how often they are requested. The most-requested album will have
        :attr:`request_rank` == 1."""
        return self['request_rank']

    @property
    def songs(self):
        """A list of :class:`RainwaveSong` objects in the album."""
        if 'song_objects' not in self:
            self['song_objects'] = []
            if 'songs' not in self:
                album_obj = self.channel.get_album_by_id(self.id)
                self['songs'] = album_obj['songs']
            for raw_song in self['songs']:
                new_song = self.channel.get_song_by_id(raw_song['id'])
                self['song_objects'].append(new_song)
        return self['song_objects']

    @property
    def vote_count(self):
        """The total number of election votes songs in the album have
        received."""
        return self['vote_count']

    def get_song_by_id(self, song_id):
        """ Return a :class:`RainwaveSong` for the given song ID. Raises an
        :exc:`IndexError` if there is no song with the given ID in the
        album.

        :param song_id: the ID of the desired song.
        :type song_id: int
        """

        for song in self.songs:
            if song.id == song_id:
                return song
        err = 'Album does not contain song with id: {0}'.format(song_id)
        raise IndexError(err)
