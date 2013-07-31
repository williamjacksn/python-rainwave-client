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
    def blocked(self):
        '''``True`` if the request is currently blocked. See
        :attr:`blocked_by_album` and :attr:`blocked_by_group` to determine why
        the request is blocked.'''
        return bool(self.blocked_by_album or self.blocked_by_group)

    @property
    def blocked_by_album(self):
        '''``True`` if the request is currently blocked because a song from the
        same album is in an election.'''
        return self._raw_info[u'album_electionblock']

    @property
    def blocked_by_group(self):
        '''``True`` if the request is currently blocked because a song from the
        same cooldown group is in an election.'''
        return self._raw_info[u'group_electionblock']

    @property
    def requestq_id(self):
        '''The request queue ID of the song in the authenticating listener's
        request queue. Used to change, reorder, or delete a request.'''
        return self._raw_info[u'requestq_id']

    def delete(self):
        '''Remove the requested song from the authenticating listener's request
        queue.'''
        self.album.channel.delete_request(self.requestq_id)


class RainwaveUserRequestQueue(list):
    '''A :class:`RainwaveUserRequestQueue` is a list-like object that supports
    explicit reordering.'''

    def __init__(self, channel):
        super(RainwaveUserRequestQueue, self).__init__()
        self.channel = channel

    def reorder(self, order):
        '''Change the order of the requests in the queue.

        :param order: the indices of the requests in the new order.
        :type order: sequence

        Example usage:

        If you have four songs in your request queue and you want to move the
        last song to the top of the queue::

        >>> from gutter import RainwaveClient
        >>> rw = RainwaveClient(5049, u'abcde12345')
        >>> game = rw.channels[0]
        >>> rq = game.user_requests
        >>> rq.reorder([3, 0, 1, 2])

        To randomly shuffle your request queue::

        >>> import random
        >>> indices = range(len(game.user_requests))
        >>> random.shuffle(indices)
        >>> rq.reorder(indices)

        All indices must appear in ``order`` and each index must only appear
        once.
        '''

        if set(order) != set(range(len(self))):
            raise Exception(u'Incorrect indices.')
        if len(order) != len(set(order)):
            raise Exception(u'Too many indices.')
        rqids = u','.join([str(self[i].requestq_id) for i in order])
        self.channel.reorder_requests(rqids)
