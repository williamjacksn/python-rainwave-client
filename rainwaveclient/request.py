from __future__ import unicode_literals

from . import song


class RainwaveRequest(song.RainwaveSong):
    """A :class:`RainwaveRequest` object is a subclass of :class:`RainwaveSong` representing a song that has been
    requested to play on the radio."""

    @classmethod
    def request_from_song(cls, _song, requester):
        request = cls(_song.album, dict(_song.items()))
        request['requester'] = requester
        return request

    def __repr__(self):
        return '<RainwaveRequest [{0}]>'.format(self)

    @property
    def requester(self):
        """The :class:`RainwaveListener` who made the request."""
        return self['requester']


class RainwaveUserRequest(song.RainwaveSong):
    """A :class:`RainwaveUserRequest` object is a subclass of :class:`RainwaveSong` representing a song in the
    authenticating listener's requests queue."""

    def __repr__(self):
        return '<RainwaveUserRequest [{0}]>'.format(self)

    @property
    def blocked(self):
        """``True`` if the request is currently blocked. See :attr:`blocked_by_album` and :attr:`blocked_by_category` to
        determine why the request is blocked."""
        return bool(self.blocked_by_album or self.blocked_by_category)

    @property
    def blocked_by_album(self):
        """``True`` if the request is currently blocked because a song from the same album is in an election."""
        return self['elec_blocked_by'] == 'album'

    @property
    def blocked_by_category(self):
        """``True`` if the request is currently blocked because a song from the same category is in an election."""
        return self['elec_blocked_by'] == 'group'

    def delete(self):
        """Remove the requested song from the authenticating listener's request queue."""
        self.album.channel.delete_request(self.id)


class RainwaveUserRequestQueue(list):
    """A :class:`RainwaveUserRequestQueue` is a list-like object that supports explicit reordering."""

    def __init__(self, channel):
        self._channel = channel
        super(RainwaveUserRequestQueue, self).__init__()

    def clear(self):
        """Clear all requests from the queue."""
        d = self._channel.clear_requests()

    def reorder(self, order):
        """Change the order of the requests in the queue.

        :param order: the indices of the requests in the new order.
        :type order: sequence

        Example usage:

        If you have four songs in your request queue and you want to move the last song to the top of the queue::

        >>> from rainwaveclient import RainwaveClient
        >>> rw = RainwaveClient(5049, 'abcde12345')
        >>> game = rw.channels[0]
        >>> rq = game.user_requests
        >>> rq.reorder([3, 0, 1, 2])

        To randomly shuffle your request queue::

        >>> import random
        >>> indices = range(len(game.user_requests))
        >>> random.shuffle(indices)
        >>> rq.reorder(indices)

        All indices must appear in ``order`` and each index must only appear once.
        """

        if set(order) != set(range(len(self))):
            raise Exception('Incorrect indices.')
        if len(order) != len(set(order)):
            raise Exception('Wrong number of indices.')
        song_ids = ','.join([str(self[i].id) for i in order])
        self._channel.reorder_requests(song_ids)
