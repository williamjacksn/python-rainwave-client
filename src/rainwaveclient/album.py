import datetime
import typing

from .category import RainwaveCategory

if typing.TYPE_CHECKING:
    from . import RainwaveChannel, RainwaveSong


class RainwaveAlbum(dict):
    """A :class:`RainwaveAlbum` object represents one album.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.albums`.
    """

    def __init__(self, channel: "RainwaveChannel", raw_info: dict) -> None:
        self._channel = channel
        super().__init__(raw_info)

    def __repr__(self) -> str:
        return f"<RainwaveAlbum [{self.channel.name} // {self.name}]>"

    def __str__(self) -> str:
        return f"{self.channel.name} // {self.name}"

    def _update(self) -> None:
        self.update(self.channel.get_album_by_id(self.id))

    @property
    def art(self) -> str:
        """The URL of the cover art for the album."""
        if "art" not in self:
            self._update()
        return self.channel.client.art_fmt.format(self["art"])

    @property
    def added_on(self) -> datetime.datetime:
        """A :class:`datetime.datetime` object specifying when the album was
        added to the playlist."""
        if "added_on" not in self:
            self._update()
        return datetime.datetime.fromtimestamp(self["added_on"], datetime.timezone.utc)

    @property
    def categories(self) -> list["RainwaveCategory"]:
        """A list of :class:`RainwaveCategory` objects representing the
        categories the songs on the album belong to."""
        if "category_objects" not in self:
            self["category_objects"] = []
            if "genres" not in self:
                self._update()
            for raw_cat in self["genres"]:
                category_id = raw_cat["id"]
                name = raw_cat["name"]
                cat = RainwaveCategory(self.channel, category_id, name)
                self["category_objects"].append(cat)
        return self["category_objects"]

    @property
    def channel(self) -> "RainwaveChannel":
        """The :class:`RainwaveChannel` object the album belongs to."""
        return self._channel

    @property
    def cool(self) -> bool:
        """A boolean representing whether the entire album is on cooldown.
        :attr:`cool` will be `True` if and only if every song on the album is on
        cooldown."""
        return self["cool"]

    @property
    def cool_lowest(self) -> datetime.datetime:
        """A :class:`datetime.datetime` object specifying the earliest date and
        time a song on the album will be out of cooldown and available to play.
        If any song on the album is already available, :attr:`cool_lowest` will
        be in the past."""
        return datetime.datetime.fromtimestamp(
            self["cool_lowest"], datetime.timezone.utc
        )

    @property
    def fave(self) -> bool:
        """A boolean representing whether the album is marked as a favourite or
        not. Change whether the album is a favourite by assigning a boolean
        value to this attribute."""
        return self.get("fave", False)

    @fave.setter
    def fave(self, value: bool) -> None:
        value = bool(value)
        if value == self.fave:
            return
        d = self.channel.fave_album(self.id, str(value).lower())
        if d["fave_album_result"]["success"]:
            self["fave"] = value
        else:
            raise Exception(d["fave_album_result"]["text"])

    @property
    def fave_count(self) -> int:
        """The number of listeners who have marked the album as a favourite."""
        if "fave_count" not in self:
            self._update()
        return self["fave_count"]

    @property
    def id(self) -> int:
        """The ID of the album."""
        return self["id"]

    @property
    def name(self) -> str:
        """The name of the album."""
        return self["name"]

    @property
    def played_last(self) -> datetime.datetime:
        """A :class:`datetime.datetime` object specifying the most recent date
        and time when a song on the album played."""
        if "played_last" not in self:
            self._update()
        return datetime.datetime.fromtimestamp(
            self["played_last"], datetime.timezone.utc
        )

    @property
    def rating(self) -> float:
        """The average of all ratings given to songs on the album by only the
        listener authenticating to the API."""
        return self["rating_user"]

    @property
    def rating_avg(self) -> float:
        """The average of all ratings given to songs on the album by all
        listeners."""
        return self["rating"]

    @property
    def rating_complete(self) -> bool:
        """A boolean representing whether the listener has rated all songs on
        the album."""
        return self["rating_complete"]

    @property
    def rating_count(self) -> int:
        """The total number of ratings given to songs on the album by all
        listeners."""
        if "rating_count" not in self:
            self._update()
        return self["rating_count"]

    @property
    def rating_histogram(self) -> dict[str, int]:
        """A dictionary representing the distribution of ratings given to all
        songs on the album by all listeners. For example::

            >>> album.rating_histogram
            {'1.0': 4, '1.5': 4, '2.0': 6, ..., '4.5': 46, '5.0': 26}
        """
        if "rating_histogram" not in self:
            self._update()
        return self["rating_histogram"]

    @property
    def rating_rank(self) -> int:
        """The position of the album when albums on the channel are ranked by
        rating. The highest-rated album will have :attr:`rating_rank` == 1."""
        if "rating_rank" not in self:
            self._update()
        return self["rating_rank"]

    @property
    def rating_user(self) -> float:
        """See :attr:`rating`."""
        return self.rating

    @property
    def request_count(self) -> int:
        """The total number of times a song on the album was requested by any
        listener."""
        if "request_count" not in self:
            self._update()
        return self["request_count"]

    @property
    def request_rank(self) -> int:
        """The position of the album when albums on the channel are ranked by
        how often they are requested. The most-requested album will have
        :attr:`request_rank` == 1."""
        if "request_rank" not in self:
            self._update()
        return self["request_rank"]

    @property
    def songs(self) -> list["RainwaveSong"]:
        """A list of :class:`RainwaveSong` objects on the album."""
        if "song_objects" not in self:
            self["song_objects"] = []
            if "songs" not in self:
                self._update()
            for raw_song in self["songs"]:
                new_song = self.channel.get_song_by_id(raw_song["id"])
                self["song_objects"].append(new_song)
        return self["song_objects"]

    @property
    def url(self) -> str:
        """The URL of the album information page on https://rainwave.cc/"""
        return f"{self.channel.url}#!/album/{self.id}"

    @property
    def vote_count(self) -> int:
        """The total number of election votes songs on the album have
        received."""
        if "vote_count" not in self:
            self._update()
        return self["vote_count"]

    def get_song_by_id(self, song_id: int) -> "RainwaveSong":
        """Return a :class:`RainwaveSong` for the given song ID. Raises an
        :exc:`IndexError` if there is no song with the given ID on the
        album.

        :param song_id: the ID of the desired song.
        :type song_id: int
        """

        for song in self.songs:
            if song.id == song_id:
                return song
        err = f"Album does not contain song with id: {song_id}"
        raise IndexError(err)
