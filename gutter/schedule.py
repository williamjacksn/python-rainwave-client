import datetime
import song


class RainwaveSchedule(object):
    '''A :class:`RainwaveSchedule` object represents an event on a
    channel.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.schedule_current`,
        :attr:`RainwaveChannel.schedule_next`, or
        :attr:`RainwaveChannel.schedule_history`.
    '''

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
        '''The ID of the event.'''
        return self._raw_info[u'sched_id']

    @property
    def starttime(self):
        '''The start time of the event in UTC time.'''
        ts = self._raw_info[u'sched_starttime']
        return datetime.datetime.utcfromtimestamp(ts)


class RainwaveElection(RainwaveSchedule):
    '''A :class:`RainwaveElection` object is a subclass of
    :class:`RainwaveSchedule` and represents an election event on a channel.'''

    def __init__(self, channel, raw_info):
        super(RainwaveElection, self).__init__(channel, raw_info)

    def __repr__(self):
        return '<RainwaveElection [{}]>'.format(self.channel.name)

    @property
    def candidates(self):
        '''A list of :class:`RainwaveCandidate` objects in the election.'''
        if not hasattr(self, '_candidates'):
            self._candidates = []
            for raw_song in self._raw_info[u'song_data']:
                tmp_album = self.channel.get_album_by_id(raw_song[u'album_id'])
                tmp_song = song.RainwaveCandidate(tmp_album, dict(raw_song))
                self._candidates.append(tmp_song)
        return self._candidates

    @property
    def songs(self):
        '''See :attr:`candidates`.'''
        return self.candidates
