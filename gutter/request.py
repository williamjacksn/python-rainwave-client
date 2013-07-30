import song


class RainwaveRequest(song.RainwaveSong):
    '''A :class:`RainwaveRequest` object is a subclass of
    :class:`RainwaveSong` representing a song that has been requested to play
    on the radio.'''

    def __init__(self, album, raw_info):
        song_info = dict(raw_info[u'request'].items())
        del raw_info[u'request']
        request_info = dict(raw_info.items() + song_info.items())
        super(RainwaveRequest, self).__init__(album, request_info)

    def __repr__(self):
        return '<RainwaveRequest [{}]>'.format(self)

    @property
    def request_id(self):
        '''The ID of the request.'''
        return self._raw_info[u'request_id']

    @property
    def requested_by(self):
        '''The :class:`RainwaveListener` who made the request.'''
        id = self._raw_info[u'request_user_id']
        return self.album.channel.get_listener_by_id(id)


class RainwaveUserRequest(song.RainwaveSong):
    '''A :class:`RainwaveUserRequest` object is a subclass of
    :class:`RainwaveSong` representing a song in the authenticating listener's
    requests queue.'''

    def __repr__(self):
        return '<RainwaveUserRequest [{}]>'.format(self)

    @property
    def requestq_id(self):
        '''The request queue ID of the song in the authenticating listener's
        request queue. Used to change, reorder, or delete a request.'''
        return self._raw_info[u'requestq_id']

    def delete(self):
        '''Remove the requested song from the authenticating listener's request
        queue.'''
        self.album.channel.delete_request(self.requestq_id)
