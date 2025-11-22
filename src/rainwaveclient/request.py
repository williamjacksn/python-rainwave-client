import typing

from .song import RainwaveSong

if typing.TYPE_CHECKING:
    from . import RainwaveChannel, RainwaveListener


class RainwaveRequest(RainwaveSong):
    """A :class:`RainwaveRequest` object is a subclass of :class:`RainwaveSong`
    representing a song that has been requested to play on the radio."""

    @classmethod
    def request_from_song(
        cls, _song: RainwaveSong, requester: "RainwaveListener"
    ) -> "RainwaveRequest":
        request = cls(_song.album, dict(_song.items()))
        request["requester"] = requester
        return request

    def __repr__(self) -> str:
        return f"<RainwaveRequest [{self}]>"

    @property
    def requester(self) -> "RainwaveListener":
        """The :class:`RainwaveListener` who made the request."""
        return self["requester"]


class RainwaveUserRequest(RainwaveSong):
    """A :class:`RainwaveUserRequest` object is a subclass of
    :class:`RainwaveSong` representing a song in the authenticating listener's
    requests queue."""

    def __repr__(self) -> str:
        return f"<RainwaveUserRequest [{self}]>"

    @property
    def blocked(self) -> bool:
        """``True`` if the request is currently blocked. See
        :attr:`blocked_by_album` and :attr:`blocked_by_category` to determine
        why the request is blocked."""
        return bool(self.blocked_by_album or self.blocked_by_category)

    @property
    def blocked_by_album(self) -> bool:
        """``True`` if the request is currently blocked because a song from the
        same album is in an election."""
        return self["elec_blocked_by"] == "album"

    @property
    def blocked_by_category(self) -> bool:
        """``True`` if the request is currently blocked because a song from the
        same category is in an election."""
        return self["elec_blocked_by"] == "group"

    def delete(self) -> None:
        """Remove the requested song from the authenticating listener's request
        queue."""
        self.album.channel.delete_request(self.id)


class RainwaveUserRequestQueue(list):
    """A :class:`RainwaveUserRequestQueue` is a list-like object that supports
    explicit reordering."""

    def __init__(self, channel: "RainwaveChannel") -> None:
        self._channel = channel
        super().__init__()

    def clear(self) -> None:
        """Clear all requests from the queue."""
        self._channel.clear_requests()

    def reorder(self, order: list[int]) -> None:
        """Change the order of the requests in the queue.

        :param order: the indices of the requests in the new order.
        :type order: sequence

        Example usage:

        If you have four songs in your request queue, and you want to move the
        last song to the top of the queue::

        >>> from rainwaveclient import RainwaveClient
        >>> rw = RainwaveClient(5049, 'abcde12345')
        >>> game = rw.channels[0]
        >>> rq = game.user_requests
        >>> rq.reorder([3, 0, 1, 2])

        To randomly shuffle your request queue::

        >>> import random
        >>> indices = list(range(len(game.user_requests)))
        >>> random.shuffle(indices)
        >>> rq.reorder(indices)

        All indices must appear in ``order`` and each index must only appear
        once.
        """

        if set(order) != set(range(len(self))):
            raise Exception("Incorrect indices.")
        if len(order) != len(set(order)):
            raise Exception("Wrong number of indices.")
        song_ids = ",".join([str(self[i].id) for i in order])
        self._channel.reorder_requests(song_ids)
