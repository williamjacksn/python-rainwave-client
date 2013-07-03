import datetime

import album
import song

class RainwaveSchedule(object):
    '''A :class:`RainwaveSchedule` object represents a voting event on a
    channel.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.schedule_current`,
        :attr:`RainwaveChannel.schedule_next`, or
        :attr:`RainwaveChannel.schedule_history`.

    :param client: the :class:`RainwaveClient` parent object.
    :param channel: the :class:`RainwaveChannel` the schedule belongs to
    :param raw_info: a dictionary of information provided by the API that
        describes the schedule.
    '''

    def __init__(self, client, channel, raw_info):
       self._client = client
       self.channel = channel
       self._raw_info = raw_info
    
    def __repr__(self):
        return u'RainwaveSchedule({})'.format(self.channel.name)

    def __str__(self):
        return repr(self)

    @property
    def starttime(self):
        '''The start time of the voting event in UTC time.'''
        ts = self._raw_info[u'sched_starttime']
        return datetime.datetime.utcfromtimestamp(ts)
    
    @property
    def songs(self):
        '''A list of the songs for the voting event.'''
        if not hasattr(self, '_songs'):
            self._songs = []
            for raw_info in self._raw_info[u'song_data']:
                tmp_album = album.RainwaveAlbum(self.channel, dict(raw_info))
                tmp_song = song.RainwaveSong(tmp_album, dict(raw_info))
                self._songs.append(tmp_song)
        return self._songs
