from __future__ import unicode_literals

import datetime

from . import song


class RainwaveSchedule(dict):
    """A :class:`RainwaveSchedule` object represents an event on a channel.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.schedule_current`,
        :attr:`RainwaveChannel.schedule_next`, or
        :attr:`RainwaveChannel.schedule_history`.
    """

    def __init__(self, channel, raw_info):
        self._channel = channel
        super(RainwaveSchedule, self).__init__(raw_info)

    def __repr__(self):
        return '<RainwaveSchedule [{0}]>'.format(self.channel.name)

    def __str__(self):
        return repr(self)

    @property
    def channel(self):
        """The :class:`RainwaveChannel` object the event belongs to."""
        return self._channel

    @property
    def id(self):
        """The ID of the event."""
        return self['id']

    @property
    def start(self):
        """A `datetime.datetime` object representing the start time of the event
        in UTC time."""
        return datetime.datetime.utcfromtimestamp(self['start'])


class RainwaveElection(RainwaveSchedule):
    """A :class:`RainwaveElection` object is a subclass of
    :class:`RainwaveSchedule` and represents an election event on a channel."""

    def __repr__(self):
        return '<RainwaveElection [{0}]>'.format(self.channel.name)

    @property
    def candidates(self):
        """A list of :class:`RainwaveCandidate` objects in the election."""
        if 'candidate_objects' not in self:
            self['candidate_objects'] = []
            for raw_song in self['songs']:
                alb = self.channel.get_album_by_id(raw_song['albums'][0]['id'])
                tmp_song = song.RainwaveCandidate(alb, raw_song)
                self['candidate_objects'].append(tmp_song)
        return self['candidate_objects']

    @property
    def songs(self):
        """See :attr:`candidates`."""
        return self.candidates


class RainwaveOneTimePlay(RainwaveSchedule):
    """A :class:`RainwaveOneTimePlay` object is a subclass of
    :class:`RainwaveSchedule` and represents a song added directly to the
    timeline by a manager."""

    def __repr__(self):
        return '<RainwaveOneTimePlay [{0}]>'.format(self.channel.name)

    @property
    def name(self):
        """The name of the event."""
        return '{0} Power Hour'.format(self['name'])

    @property
    def song(self):
        """The :class:`RainwaveSong` for the event."""
        album_id = self['songs'][0]['albums'][0]['id']
        tmp_album = self.channel.get_album_by_id(album_id)
        return song.RainwaveSong(tmp_album, self['songs'][0])
