import datetime
import typing

from .song import RainwaveCandidate, RainwaveSong

if typing.TYPE_CHECKING:
    from . import RainwaveChannel


class RainwaveSchedule(dict):
    """A :class:`RainwaveSchedule` object represents an event on a channel.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.schedule_current`,
        :attr:`RainwaveChannel.schedule_next`, or
        :attr:`RainwaveChannel.schedule_history`.
    """

    def __init__(self, channel: "RainwaveChannel", raw_info: dict) -> None:
        self._channel = channel
        super().__init__(raw_info)

    def __len__(self) -> int:
        return self["length"]

    def __repr__(self) -> str:
        return f"<RainwaveSchedule [{self.channel.name}]>"

    def __str__(self) -> str:
        return repr(self)

    @property
    def channel(self) -> "RainwaveChannel":
        """The :class:`RainwaveChannel` object the event belongs to."""
        return self._channel

    @property
    def end(self) -> datetime.datetime:
        """A `datetime.datetime` object representing the end time of the event. For
        future events, this should equal :attr:`start` + :attr:`length`. For current and
        past events this should equal :attr:`start_actual` + :attr:`length`."""
        return datetime.datetime.fromtimestamp(self["end"], datetime.timezone.utc)

    @property
    def id(self) -> int:
        """The ID of the event."""
        return self["id"]

    @property
    def length(self) -> int:
        """The duration of the event in seconds. For future elections, this value is
        estimated by averaging the duration of all songs in the election.
        :class:`RainwaveSchedule` objects also support `len(schedule)`."""
        return len(self)

    @property
    def start(self) -> datetime.datetime:
        """A `datetime.datetime` object representing the estimated start time of the
        event. This is only useful for future events. For current and past events, see
        :attr:`start_actual`."""
        return datetime.datetime.fromtimestamp(self["start"], datetime.timezone.utc)

    @property
    def start_actual(self) -> datetime.datetime:
        """A `datetime.datetime` object representing the actual start time of the event.
        If the event has not started yet, this will be `None`."""
        if self["start_actual"] is not None:
            return datetime.datetime.fromtimestamp(
                self["start_actual"], datetime.timezone.utc
            )

    @property
    def type(self) -> str:
        """The type of event (e.g. `Election` or `OneUp`)."""
        return self["type"]


class RainwaveElection(RainwaveSchedule):
    """A :class:`RainwaveElection` object is a subclass of
    :class:`RainwaveSchedule` and represents an election event on a channel."""

    def __repr__(self) -> str:
        return f"<RainwaveElection [{self.channel.name}]>"

    @property
    def candidates(self) -> list["RainwaveCandidate"]:
        """A list of :class:`RainwaveCandidate` objects in the election."""
        if "candidate_objects" not in self:
            self["candidate_objects"] = []
            for raw_song in self["songs"]:
                alb = self.channel.get_album_by_id(raw_song["albums"][0]["id"])
                tmp_song = RainwaveCandidate(alb, self, raw_song)
                self["candidate_objects"].append(tmp_song)
        return self["candidate_objects"]

    @property
    def song(self) -> "RainwaveCandidate":
        """The first :class:`RainwaveCandidate` object in the list of
        candidates. If the :class:`RainwaveElection` event has already closed,
        this is the song that won the election."""
        return self.candidates[0]

    @property
    def songs(self) -> list["RainwaveCandidate"]:
        """See :attr:`candidates`."""
        return self.candidates


class RainwaveOneTimePlay(RainwaveSchedule):
    """A :class:`RainwaveOneTimePlay` object is a subclass of
    :class:`RainwaveSchedule` and represents a song added directly to the
    timeline by a manager."""

    def __repr__(self) -> str:
        return f"<RainwaveOneTimePlay [{self.channel.name}]>"

    @property
    def name(self) -> str:
        """The name of the event."""
        _name = self.get("name")
        return f"{_name} Power Hour"

    @property
    def song(self) -> RainwaveSong:
        """The :class:`RainwaveSong` for the event."""
        album_id = self["songs"][0]["albums"][0]["id"]
        tmp_album = self.channel.get_album_by_id(album_id)
        return RainwaveSong(tmp_album, self["songs"][0])

    @property
    def songs(self) -> list[RainwaveSong]:
        """A list containing the :class:`RainwaveSong` for the event."""
        return [self.song]
