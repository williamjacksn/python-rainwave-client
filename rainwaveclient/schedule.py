import datetime

from . import song


class RainwaveSchedule:
    """A :class:`RainwaveSchedule` object represents an event on a
    channel.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.schedule_current`,
        :attr:`RainwaveChannel.schedule_next`, or
        :attr:`RainwaveChannel.schedule_history`.
    """

    #: The :class:`RainwaveChannel` object the event belongs to.
    channel = None

    def __init__(self, channel, raw_info):
        self.channel = channel
        self._raw_info = raw_info

    def __repr__(self):
        return '<RainwaveSchedule [{}]>'.format(self.channel.name)

    def __str__(self):
        return repr(self)

    @property
    def id(self):
        """The ID of the event."""
        return self._raw_info['sched_id']

    @property
    def starttime(self):
        """The start time of the event in UTC time."""
        ts = self._raw_info['sched_starttime']
        return datetime.datetime.utcfromtimestamp(ts)


class RainwaveElection(RainwaveSchedule):
    """A :class:`RainwaveElection` object is a subclass of
    :class:`RainwaveSchedule` and represents an election event on a channel."""

    def __init__(self, channel, raw_info):
        super(RainwaveElection, self).__init__(channel, raw_info)

    def __repr__(self):
        return '<RainwaveElection [{}]>'.format(self.channel.name)

    @property
    def candidates(self):
        """A list of :class:`RainwaveCandidate` objects in the election."""
        if not hasattr(self, '_candidates'):
            self._candidates = []
            for raw_song in self._raw_info['song_data']:
                tmp_album = self.channel.get_album_by_id(raw_song['album_id'])
                tmp_song = song.RainwaveCandidate(tmp_album, dict(raw_song))
                self._candidates.append(tmp_song)
        return self._candidates

    @property
    def songs(self):
        """See :attr:`candidates`."""
        return self.candidates


class RainwaveOneTimePlay(RainwaveSchedule):
    """A :class:`RainwaveOneTimePlay` object is a subclass of
    :class:`RainwaveSchedule` and represents a song added directly to the
    timeline by a manager."""

    def __init__(self, channel, raw_info):
        return super(RainwaveOneTimePlay, self).__init__(channel, raw_info)

    def __repr__(self):
        return '<RainwaveOneTimePlay [{}]>'.format(self.channel.name)

    @property
    def added_by(self):
        """The :class:`RainwaveListener` who added the song to the timeline."""
        return self.channel.get_listener_by_id(self._raw_info['user_id'])

    @property
    def song(self):
        """The :class:`RainwaveSong` for the event."""
        album_id = self._raw_info['song_data'][0]['album_id']
        tmp_album = self.channel.get_album_by_id(album_id)
        return song.RainwaveSong(tmp_album, self._raw_info['song_data'][0])
